from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Work, Artist, Renter
from .forms import WorkForm, SaleForm, ArtistForm, RenterForm

from io import BytesIO
import datetime
from datetime import datetime
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# Reportlab imports
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont







# Create your views here.
# @login_required(login_url="login-page")
# def artist_slide_page(request, slug):
#     selected = Work.objects.get(slug=slug)
#     artist = Artist.objects.filter(work__slug=slug)
#     works = Work.objects.filter(artist__slug=slug)

#     content = {
#         "artist": artist,
#         "works": works,
#         "selected": selected,
        
#     }
#     return render(request, "databank/artist_slider.html", content)


@login_required(login_url="login-page")
def create_invoice(request):
    if request.method == "POST":
        work_id = request.POST.getlist("sale-checkbox")
        pk = work_id[0]
        work = Work.objects.get(pk=pk)
        invoice_number = request.POST["invoice-number"]
        address = request.POST["address"]
        plz = request.POST["plz"]
        city = request.POST["city"]
        details = request.POST["details"]

        

        # return HttpResponse(f"This worked {work, invoice_number}")

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        c.translate(cm, cm)
        
        current_date = datetime.now()
        formatted_date = current_date.strftime("%d.%m.%Y")

        # Register custom font
        font_path = 'databank/static/WeissenhofGrotesk-Light.ttf'
        Weiss_Light = 'WeissenhofGrotesk-Light'

        font_path2 = 'databank/static/WeissenhofGrotesk-Medium.ttf'
        Weiss_Medium = 'WeissenhofGrotesk-Medium'


        pdfmetrics.registerFont(TTFont(Weiss_Light, font_path))
        pdfmetrics.registerFont(TTFont(Weiss_Medium, font_path2))

        c.setFont(Weiss_Light, 12)
        c.setStrokeColorRGB(0.8, 0.8, 0.8)

        # Header
        c.drawImage(f"databank/static/databank/images/gpp_logo_02.jpg",
                    cm, 25.4*cm, width=66, height=66)
        c.drawString(12.5*cm, 27.4*cm, "Friedrich–Ebert-Straße  143e")
        c.drawString(12.5*cm, 26.9*cm, "Ger                42117, Wuppertal")
        c.drawString(12.5*cm, 26.4*cm, "phone:    +49 (0) 173 26 11115")
        c.drawString(12.5*cm, 25.9*cm, "      groelle(at)passprojects.de")
        c.drawString(12.5*cm, 25.4*cm, "                         www.groelle.de")

        # Seperator
        # c.setLineWidth(1)
        c.line(x1=1*cm, y1=24.9*cm, x2=18*cm, y2=24.9*cm)

        # Contact Data
        c.setFont(Weiss_Medium, 12)
        c.drawString(1*cm, 24*cm, f"{work.buyer}")
        c.setFont(Weiss_Light, 12)
        c.drawString(1*cm, 23.5*cm, f"{address}")
        c.drawString(1*cm, 23*cm, f"{plz} {city}")

        # Invoice Information
        c.setLineWidth(1)
        c.rect(1*cm, 20.8*cm, 17*cm, 0.7*cm, fill=0)
        c.setFont(Weiss_Medium, 12)
        c.drawString(1.2*cm, 21*cm, f"INVOICE {invoice_number}")
        c.drawString(15.7*cm, 21*cm, f"{formatted_date}")

        c.setFont(Weiss_Light, 12)
        # Dynamic Paragraph
        style = getSampleStyleSheet()["Normal"]
        text = f"Wir danken Ihnen für den Kauf der Arbeit von {work.artist.name}. <br/><br/>  {details}"

        p1 = Paragraph(text, style=style)
        p1.wrapOn(c, 480, 200)
        x, y = 1*cm, 20*cm - p1.height
        p1.drawOn(c, x, y)

        img = f"uploads/{work.image}"
        # img="horizontal.jpg"
        img_reader = ImageReader(img)

        img_width_px, img_height_px = img_reader.getSize()

        img_width_cm = img_width_px / 28.3464567
        img_height_cm = img_height_px / 28.3464567

        if img_width_cm > img_height_cm:
            aspect_ratio = img_height_cm / img_width_cm
            target_width = 7*cm
            target_height = aspect_ratio * target_width

            c.setFont(Weiss_Medium, 12)
            c.drawString(10*cm, 11.5*cm, f"{work.name}")
            c.setFont(Weiss_Light, 12)
            c.drawString(10*cm, 11*cm, f"{work.production_date}")
            c.drawString(10*cm, 10.5*cm, f"{work.materials}")
            c.drawString(
                10*cm, 10*cm, f"{work.width} x {work.height} cm")

        else:
            aspect_ratio = img_width_cm / img_height_cm
            target_height = 7*cm
            target_width = aspect_ratio * target_height

            c.setFont(Weiss_Medium, 12)
            c.drawString(8*cm, 11.5*cm, f"{work.name}")
            c.setFont(Weiss_Light, 12)
            c.drawString(8*cm, 11*cm, f"{work.production_date}")
            c.drawString(8*cm, 10.5*cm, f"{work.materials}")
            c.drawString(
                8*cm, 10*cm, f"{work.width} x {work.height} cm")

        c.drawImage(img, 2*cm, 10*cm, target_width, target_height)

        # Price data
        c.rect(1*cm, 1.5*cm, 17*cm, 5.2*cm, fill=0)
        c.line(x1=1.2*cm, y1=3*cm, x2=17.8*cm, y2=3*cm)

        # Labels
        c.setFont(Weiss_Medium, 12)
        c.drawString(1.2*cm, 6*cm, "Listenpreis:")
        c.setFont(Weiss_Light, 12)
        c.drawString(1.2*cm, 5*cm, "Netto:")
        if work.decree > 0:
            c.drawString(1.2*cm, 4.5*cm, f"abzgl. {work.decree}%:")
        c.drawString(1.2*cm, 3.5*cm, f"zzgl. {work.tax}% MwSt:")

        c.setFont(Weiss_Medium, 12)
        c.drawString(1.2*cm, 2.3*cm, "Total:")

        # Prices calculations
        list_price = f"{round(work.price,2)} €"
        list_price_width = c.stringWidth(list_price)
        lx = c._pagesize[0] - list_price_width - 3.5*cm

        if work.tax == 19:
            price = work.price / 1.19
        else:
            price = work.price / 1.07

        netto = round(price, 2)

        netto_price = f"{netto} €"
        netto_price_width = c.stringWidth(netto_price)
        nx = c._pagesize[0] - netto_price_width - 3.5*cm


        decree_amount = netto * (work.decree/100)
        decree = f"-{round(decree_amount,2)} €"
        decree_width = c.stringWidth(decree)
        dx = c._pagesize[0] - decree_width - 3.5*cm

        final_netto = netto - decree_amount
        tax_amount = final_netto * (work.tax/100)
        tax = f"+{round(tax_amount,2)} €"
        tax_width = c.stringWidth(tax)
        tx = c._pagesize[0] - tax_width - 3.5*cm


        decree_rate = {
            5: 1.05,
            10: 1.10,
            15: 1.15,
            20: 1.20,
        }


        total = final_netto + tax_amount

        if work.decree > 0:
            total_price = f"{round(total,2)} €"
        else:
            total_price = f"{work.price} €"
        total_price_width = c.stringWidth(total_price)
        tox = c._pagesize[0] - total_price_width - 3.5*cm

        # Drawn prices
        c.drawString(lx, 6*cm, list_price)
        c.setFont(Weiss_Light, 12)
        c.drawString(nx, 5*cm, netto_price)
        if work.decree > 0:
            c.drawString(dx, 4.5*cm, decree)
        c.drawString(tx, 3.5*cm, tax)

        c.setFont(Weiss_Medium, 12)
        c.drawString(tox, 2.3*cm, total_price)

        # Footer
        c.setFont(Weiss_Light, 8)
        c.drawString(
            2.5*cm, 0.1*cm, "Jürgen Grölle | Finanzamt Wuppertal | StNr. 132/5968/1099 | BIC : WUPSDE33XXX. | DE39 3305 0000 0006 4440 61")



        c.showPage()
        c.save()
        buffer.seek(0)

        return FileResponse(buffer, filename=f"Rechnung_{invoice_number}.pdf")



@login_required(login_url="login-page")
def create_pricelist(request):
    if request.method == "POST":
        works = request.POST.getlist("art-work")
        exhibition_title = request.POST['exhibition_title']

        if len(works) < 1:
            return redirect("databank-page")

        artist_names = []
        current_year = datetime.now().year
        selected = Work.objects.filter(pk__in=works)

        for work in selected:
            if work.artist.name not in artist_names:
                artist_names.append(work.artist.name)

        names = " | ".join(name for name in artist_names)

        content = {"selected": selected,
                   "year": current_year,
                   "names": names,
                   "exhibition_title": exhibition_title,
                   }

        template_path = "databank/pricelist_template.html"
        response = HttpResponse(content_type="application/pdf")
        # if download
        # response["Content-Disposition"] = 'attachment; filename="pricelist.pdf"'
        # if display only
        response["Content-Disposition"] = f'filename="{exhibition_title}-Preisliste.pdf"'
        template = get_template(template_path)
        html = template.render(content)

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse("We had some error <pre>" + html + "</pre>")
        return response
    else:
        return redirect("databank-page")



@login_required(login_url="login-page")
def addartist_page(request):
    form = ArtistForm()
    storagetags = Artist.objects.all()

    if request.method == "POST":
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            print(request.POST)

            return redirect("databank-page")

    content = {"form": form,
               "storagetags": storagetags,}

    return render(request, "databank/addartist.html", content)



@login_required(login_url="login-page")
def addwork_page(request):
    form = WorkForm()

    if request.method == "POST":
        form = WorkForm(request.POST)
        if form.is_valid():
            form.save()
            print(request.POST)

            return redirect("databank-page")

    content = {"form": form}

    return render(request, "databank/addwork.html", content)



@login_required(login_url="login-page")
def duesseldorf_page(request):
    artists = Artist.objects.all()
    works = Work.objects.filter(storagestatus="Düsseldorf")

    content = {"artists": artists,
                "works": works,
                }

    return render(request, "databank/index.html", content)



@login_required(login_url="login-page")
def wuppertal_page(request):
    artists = Artist.objects.all()
    works = Work.objects.filter(storagestatus="Wuppertal")

    content = {"artists": artists,
                "works": works,
                }

    return render(request, "databank/index.html", content)



@login_required(login_url="login-page")
def editwork_page(request, slug):
    work = Work.objects.get(slug=slug)
    form = WorkForm(instance=work)

    # print(str(form.fields['tax']))

    if request.method == "POST":
        form = WorkForm(request.POST, request.FILES, instance=work)
        if form.is_valid():
            form.save()
            print(request.POST)

            previous_url = request.META.get('HTTP_REFERER')
            return redirect(previous_url)
            

    content = {"work": work,
               "form": form, }

    return render(request, "databank/work_edit.html", content)



@login_required(login_url="login-page")
def salework_page(request, slug):
    work = Work.objects.get(slug=slug)
    form = SaleForm(instance=work)

    if request.method == "POST":
        form = SaleForm(request.POST, request.FILES, instance=work)
        if form.is_valid():
            form.save()
            print(request.POST)

            return redirect("artistworks-page", slug=work.artist.slug)

    content = {"work": work,
               "form": form, }

    return render(request, "databank/salework_edit.html", content)



@login_required(login_url="login-page")
def artistworks_page(request, slug):
    artists = Artist.objects.all()
    works = Work.objects.filter(artist__slug=slug)

    content = {"artists": artists,
               "works": works,
               }

    return render(request, "databank/index.html", content)


@login_required(login_url="login-page")
def databank_page(request):
    artists = Artist.objects.all()
    works = Work.objects.all()
    
    content = {"artists": artists,
               "works": works,
               }
    return render(request, "databank/index.html", content)



