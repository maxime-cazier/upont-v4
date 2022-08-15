import pandas
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from social.models import Club, Student
from trade.forms import EditPrice
from trade.models import Good, Transaction
from trade.serializers import TransactionSerializer

from .forms import EditAlcohol, EditPochtronAdmin
from .models import Alcohol, PochtronAdmin
from .serializers import AlcoholSerializer


class SearchAlcohol(APIView):
    """
    API endpoint that returns the alcohols whose name contains the query.
    """

    def get(self, request):
        if "alcohol" in request.GET and request.GET["alcohol"].strip():
            query = request.GET.get("alcohol", None)
            alcohols = Alcohol.objects.filter(name__icontains=query).order_by("-name")[
                :5
            ]
        else:
            alcohols = Alcohol.objects.all().order_by("-name")[:5]
        serializer = AlcoholSerializer(alcohols, many=True)
        return Response({"alcohols": serializer.data})


@login_required
def home(request):
    context = {}
    club = get_object_or_404(Club, name="Foyer")
    student = get_object_or_404(Student, user__pk=request.user.id)

    if (
        club.is_member(student.id)
        and not PochtronAdmin.objects.filter(student=student).exists()
    ):
        # Add member of Foyer to Pochtron Admin
        admin = PochtronAdmin(student=student)
        admin.save()

    context["admin"] = PochtronAdmin.objects.filter(student=student).exists()
    context["user_balance"] = student.balance_in_euros(club)

    context["transactions"] = [
        {
            "product": t.good.name,
            "quantity": t.quantity,
            "price": t.quantity * t.good.price_at_date(t.date) / 100,
            "date": t.date,
        }
        for t in Transaction.objects.filter(student=student)
        .filter(good__club=club)
        .order_by("-date")
    ]

    return render(request, "pochtron/home.html", context)


@login_required
def admin_home_page(request):
    club = get_object_or_404(Club, name="Foyer")
    student = get_object_or_404(Student, user__pk=request.user.id)

    try:
        admin = PochtronAdmin.objects.get(student=student)
    except PochtronAdmin.DoesNotExist:
        raise PermissionDenied

    consommations = Alcohol.objects.filter(club=club)
    context = {"consommations": consommations, "admin": admin}
    return render(request, "pochtron/admin.html", context)


@login_required
def manage_accounts(request):
    student = get_object_or_404(Student, user__pk=request.user.id)

    try:
        PochtronAdmin.objects.get(student=student, credit=True)
    except PochtronAdmin.DoesNotExist:
        raise PermissionDenied

    context = {}
    return render(request, "pochtron/manage_accounts.html", context)


@login_required
def shop(request):
    context = {}
    student = get_object_or_404(Student, user__pk=request.user.id)

    try:
        PochtronAdmin.objects.get(student=student)
    except PochtronAdmin.DoesNotExist:
        raise PermissionDenied

    return render(request, "pochtron/shop.html", context)


@login_required
def conso_create(request):
    context = {"create": True}
    club = get_object_or_404(Club, name="Foyer")
    student = get_object_or_404(Student, user__pk=request.user.id)

    try:
        PochtronAdmin.objects.get(student=student, alcohol=True)
    except PochtronAdmin.DoesNotExist:
        raise PermissionDenied

    if request.method == "POST":
        conso_form = EditAlcohol(
            {
                "name": request.POST["name"],
                "degree": request.POST["degree"],
                "volume": request.POST["volume"],
                "club": club,
            },
        )
        if conso_form.is_valid():
            conso = conso_form.save()
            price_form = EditPrice(
                {"price": request.POST["price"], "date": timezone.now(), "good": conso},
            )
            if price_form.is_valid:
                price_form.save()
                return HttpResponseRedirect(reverse("pochtron:admin"))
    else:
        conso_form = EditAlcohol()
        price_form = EditPrice()
    context["EditAlcohol"] = conso_form
    context["EditPrice"] = price_form
    return render(request, "pochtron/create_consos.html", context)


@login_required
def conso_edit(request, conso_id):
    context = {"edit": True}
    club = get_object_or_404(Club, name="Foyer")
    student = get_object_or_404(Student, user__pk=request.user.id)
    conso = get_object_or_404(Alcohol, pk=conso_id)

    try:
        PochtronAdmin.objects.get(student=student, alcohol=True)
    except PochtronAdmin.DoesNotExist:
        raise PermissionDenied

    if request.method == "POST":
        conso_form = EditAlcohol(
            {
                "name": request.POST["name"],
                "degree": request.POST["degree"],
                "volume": request.POST["volume"],
                "club": club,
            },
            instance=conso,
        )
        if conso_form.is_valid():
            conso = conso_form.save()
            price_form = EditPrice(
                {"price": request.POST["price"], "date": timezone.now(), "good": conso},
            )
            if price_form.is_valid:
                price_form.save()
                return HttpResponseRedirect(reverse("pochtron:admin"))
    else:
        conso_form = EditAlcohol()
        price_form = EditPrice()
        conso_form.fields["name"].initial = conso.name
        conso_form.fields["degree"].initial = conso.degree
        conso_form.fields["volume"].initial = conso.volume
        price_form.fields["price"].initial = conso.price
    context["EditAlcohol"] = conso_form
    context["EditPrice"] = price_form
    return render(request, "pochtron/create_consos.html", context)


@login_required
def manage_admins(request):
    student = get_object_or_404(Student, user__pk=request.user.id)

    try:
        PochtronAdmin.objects.get(student=student, manage_admins=True)
    except PochtronAdmin.DoesNotExist:
        raise PermissionDenied

    context = {"admins": PochtronAdmin.objects.all()}
    return render(request, "pochtron/manage_admins.html", context)


@login_required
def admin_edit(request, admin_id):
    student = get_object_or_404(Student, user__pk=request.user.id)
    admin = get_object_or_404(PochtronAdmin, pk=admin_id)

    try:
        PochtronAdmin.objects.get(student=student, manage_admins=True)
    except PochtronAdmin.DoesNotExist:
        raise PermissionDenied

    if request.method == "POST":
        if "Supprimer" in request.POST:
            admin.delete()
            return redirect("pochtron:manage_admins")
        elif "Valider" in request.POST:
            POST = request.POST.copy()
            POST["student"] = admin.student
            admin_form = EditPochtronAdmin(POST, instance=admin)
            if admin_form.is_valid():
                admin = admin_form.save()
                return redirect("pochtron:manage_admins")
    else:
        admin_form = EditPochtronAdmin()
        admin_form.fields["student"].disabled = True
        admin_form.fields["student"].initial = admin.student
        admin_form.fields["alcohol"].initial = admin.alcohol
        admin_form.fields["credit"].initial = admin.credit
        admin_form.fields["manage_admins"].initial = admin.manage_admins

        context = {
            "Edit": True,
            "admin": admin,
            "EditPochtronAdmin": admin_form,
        }
        return render(request, "pochtron/admin_edit.html", context)


@login_required
def admin_create(request):
    student = get_object_or_404(Student, user__pk=request.user.id)

    try:
        PochtronAdmin.objects.get(student=student, manage_admins=True)
    except PochtronAdmin.DoesNotExist:
        raise PermissionDenied

    if request.method == "POST":
        if "Valider" in request.POST:
            # admin_student = None if the student is not yet related to a PochtronAdmin object
            admin_student = PochtronAdmin.objects.filter(
                student=request.POST["student"]
            ).first()
            admin_form = EditPochtronAdmin(request.POST, instance=admin_student)
            if admin_form.is_valid():
                admin_form.save()
                return redirect("pochtron:manage_admins")
    else:
        admin_form = EditPochtronAdmin()
        admin_form.fields["alcohol"].initial = False
        admin_form.fields["credit"].initial = False
        admin_form.fields["manage_admins"].initial = False

        context = {
            "Edit": False,
            "EditPochtronAdmin": admin_form,
        }
        return render(request, "pochtron/admin_edit.html", context)


class PochtronId(APIView):
    """
    API endpoint that returns the id of the club "Foyer".
    """

    def get(self, request):
        club = get_object_or_404(Club, name="Foyer")
        return Response({"id": club.id})


class TransactionsView(APIView):
    """
    API endpoint that returns the transactions data to display on a graph.
    """

    def get(self, request):
        student = get_object_or_404(Student, user__pk=request.user.id)
        club = get_object_or_404(Club, name="Foyer")
        transactions = Transaction.objects.filter(student=student, good__club=club)
        dataframe = pandas.DataFrame.from_records(
            TransactionSerializer(transactions, many=True).data, index="id"
        )
        print(dataframe)

        if "timeline" in self.request.GET and self.request.GET["timeline"].strip():
            timeline = self.request.GET.get("timeline", "year")
        else:
            timeline = "year"
        consos = Good.objects.filter(club=club)
        dataframe = dataframe.loc[
            :, dataframe.columns != "student"
        ]  # we don't need the student column
        dataframe["good_id"] = dataframe.good.apply(lambda x: x["id"])
        data = []
        for k, conso in enumerate(consos):
            current_data = dataframe.loc[dataframe.good_id == conso.id]
            if current_data.empty:
                continue
            split_date = current_data["date"].str.split(" ", expand=True)
            current_data[["day", "month", "year"]] = split_date[0].str.split(
                "-", expand=True
            )
            current_data[["hour", "minute", "second"]] = split_date[1].str.split(
                ":", expand=True
            )
            groupby = [
                current_data.year.rename("year"),
                current_data.month.rename("month"),
                current_data.day.rename("day"),
                current_data.hour.rename("hour"),
                current_data.minute.rename("minute"),
            ]
            if timeline == "hour":
                groupby = groupby[:4]
            if timeline == "day":
                groupby = groupby[:3]
            if timeline == "month":
                groupby = groupby[:2]
            if timeline == "year":
                groupby = groupby[:1]
            current_data = current_data.groupby(groupby).agg({"count"})
            current_data = current_data.loc[:, "quantity"]
            current_data["good_name"] = conso.name
            data.append(current_data)
            print(
                "===================================================================="
            )
            print(k)
            print(conso)
            print(current_data)
            print(
                "===================================================================="
            )
        return Response(pandas.concat(data))
