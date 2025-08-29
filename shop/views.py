from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Receipt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
import io
from xhtml2pdf import pisa

def product_list(request):
    return render(request, "shop/product_list.html", {"products": Product.objects.all()})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def cart(request):
    cart_ids = request.session.get('cart', [])
    cart_items = []
    total = 0
    for pid in cart_ids:
        try:
            product = Product.objects.get(id=int(pid))
            cart_items.append({'name': product.name, 'price': product.price})
            total += float(product.price)
        except Product.DoesNotExist:
            pass
    # Coupon logic
    coupon = request.session.get('coupon', 0)
    if request.method == "POST" and "set_coupon" in request.POST:
        try:
            coupon = float(request.POST.get("set_coupon", 0))
            request.session['coupon'] = coupon
        except Exception:
            request.session['coupon'] = 0
        coupon = request.session.get('coupon', 0)
    discounted_total = total
    if coupon:
        try:
            coupon = float(coupon)
            if 0 < coupon <= 100:
                discounted_total = total * (1 - coupon / 100)
        except Exception:
            discounted_total = total
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'discounted_total': discounted_total,
        'coupon': coupon,
    })

def contact(request):
    return render(request, "shop/contact.html")  # Render the contact.html template

def shop(request):
    return render(request, 'shop/shop.html')

def food(request):
    foods = Product.objects.filter(category__name__iexact='Food')
    return render(request, 'shop/food.html', {'foods': foods})

def cloth(request):
    cloths = Product.objects.filter(category__name__iexact='Cloth')
    return render(request, 'shop/cloth.html', {'cloths': cloths})

def toy(request):
    toys = Product.objects.filter(category__name__iexact='Toy')
    return render(request, 'shop/toy.html', {'toys': toys})

def carrier(request):
    carriers = Product.objects.filter(category__name__iexact='Carrier')
    return render(request, 'shop/carrier.html', {'carriers': carriers})

def medicine(request):
    medicines = Product.objects.filter(category__name__iexact='Medicine')
    return render(request, 'shop/medicine.html', {'medicines': medicines})

def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        product_id = int(product_id)
        # Only add if product exists
        try:
            product = Product.objects.get(id=product_id)
            if product_id not in cart:
                cart.append(product_id)
                request.session['cart'] = cart
                request.session.modified = True
        except Product.DoesNotExist:
            pass
        return redirect('shop:cart')
    return redirect('shop:food')

@login_required
def add_product(request):
    # Get category from query param (?category=Food, Toy, Cloth, Medicine, Carrier)
    category_name = request.GET.get('category', 'Food')
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        category, _ = Category.objects.get_or_create(name=category_name)
        image = request.FILES.get('image')
        Product.objects.create(
            name=name,
            price=price,
            category=category,
            image=image
        )
        if category_name.lower() == 'food':
            return redirect('shop:food')
        elif category_name.lower() == 'toy':
            return redirect('shop:toy')
        elif category_name.lower() == 'cloth':
            return redirect('shop:cloth')
        elif category_name.lower() == 'medicine':
            return redirect('shop:medicine')
        elif category_name.lower() == 'carrier':
            return redirect('shop:carrier')
        else:
            return redirect('shop:shop')
    return render(request, 'shop/add_product.html', {'category_name': category_name})

@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    category_name = product.category.name if product.category else 'Food'
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        if name and price:
            product.name = name
            product.price = price
            if request.FILES.get('image'):
                product.image = request.FILES['image']
            product.save()
            if category_name.lower() == 'food':
                return redirect('shop:food')
            elif category_name.lower() == 'toy':
                return redirect('shop:toy')
            elif category_name.lower() == 'cloth':
                return redirect('shop:cloth')
            elif category_name.lower() == 'medicine':
                return redirect('shop:medicine')
            elif category_name.lower() == 'carrier':
                return redirect('shop:carrier')
            else:
                return redirect('shop:shop')
        else:
            error = "Name and Price are required."
            return render(request, 'shop/update_product.html', {'product': product, 'error': error})
    return render(request, 'shop/update_product.html', {'product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    category_name = product.category.name if product.category else 'Food'
    if request.method == 'POST':
        product.delete()
        if category_name.lower() == 'food':
            return redirect('shop:food')
        elif category_name.lower() == 'toy':
            return redirect('shop:toy')
        elif category_name.lower() == 'cloth':
            return redirect('shop:cloth')
        elif category_name.lower() == 'medicine':
            return redirect('shop:medicine')
        elif category_name.lower() == 'carrier':
            return redirect('shop:carrier')
        else:
            return redirect('shop:shop')
    return render(request, 'shop/delete_product.html', {'product': product})

@login_required
def payment(request):
    payment_methods = [
        ('bkash', 'bKash', 'images/icon/bkash.png'),
        ('nagad', 'Nagad', 'images/icon/Nagad.png'),
        ('rocket', 'Rocket', 'images/icon/rocket.png'),
        ('upay', 'Upay', 'images/icon/upay.png'),
        ('dbbl', 'DBBL', 'images/icon/dbbl.jpg'),
        ('ebl', 'EBL', 'images/icon/ebl.png'),
        ('brac', 'BRAC Bank', 'images/icon/BRAC.png'),
        ('pathao', 'Pathao Pay', 'images/icon/pathao_pay.png'),
        ('paypal', 'PayPal', 'images/icon/paypal.png'),
        ('visa', 'Visa', 'images/icon/visa.png'),
        ('mastercard', 'MasterCard', 'images/icon/card.png'),
    ]
    cart_ids = request.session.get('cart', [])
    cart_items = []
    total = 0
    for pid in cart_ids:
        try:
            product = Product.objects.get(id=int(pid))
            cart_items.append({'name': product.name, 'price': product.price})
            total += float(product.price)
        except Product.DoesNotExist:
            pass
    # Coupon 
    coupon = request.session.get('coupon', 0)
    discounted_total = total
    if coupon:
        try:
            coupon = float(coupon)
            if 0 < coupon <= 100:
                discounted_total = total * (1 - coupon / 100)
        except Exception:
            discounted_total = total
    return render(request, "shop/payment.html", {
        "payment_methods": payment_methods,
        "total": discounted_total,
    })

@csrf_exempt
def payment_details(request):
    cart_ids = request.session.get('cart', [])
    cart_items = []
    total = 0
    for pid in cart_ids:
        try:
            product = Product.objects.get(id=int(pid))
            cart_items.append({'name': product.name, 'price': product.price})
            total += float(product.price)
        except Product.DoesNotExist:
            pass
    # Coupon
    coupon = request.session.get('coupon', 0)
    discounted_total = total
    if coupon:
        try:
            coupon = float(coupon)
            if 0 < coupon <= 100:
                discounted_total = total * (1 - coupon / 100)
        except Exception:
            discounted_total = total
    if request.method == "POST":
        method = request.POST.get("payment_method")
        return render(request, "shop/payment_details.html", {
            "method": method,
            "total": discounted_total,
            "cart_items": cart_items,
        })
    return redirect('shop:payment')

@login_required
def previous_orders(request):
    receipts = Receipt.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "shop/previous_orders.html", {"receipts": receipts})

@login_required
def download_receipt(request, receipt_id):
    try:
        receipt = Receipt.objects.get(id=receipt_id, user=request.user)
        return FileResponse(receipt.pdf.open('rb'), as_attachment=True, filename=f"receipt_{receipt.id}.pdf")
    except Receipt.DoesNotExist:
        raise Http404("Receipt not found.")

@csrf_exempt
def payment_success(request):
    cart_ids = request.session.get('cart', [])
    cart_items = []
    total = 0
    for pid in cart_ids:
        try:
            product = Product.objects.get(id=int(pid))
            cart_items.append({'name': product.name, 'price': product.price})
            total += float(product.price)
        except Product.DoesNotExist:
            pass
    # Coupon 
    coupon = request.session.get('coupon', 0)
    discounted_total = total
    if coupon:
        try:
            coupon = float(coupon)
            if 0 < coupon <= 100:
                discounted_total = total * (1 - coupon / 100)
        except Exception:
            discounted_total = total
    request.session['cart'] = []
    payment_method = request.POST.get("payment_method") or request.GET.get("payment_method")
    user = request.user if request.user.is_authenticated else None

    # PDF receipt
    if user:
        receipt_html = render_to_string("shop/receipt_pdf.html", {
            "user": user,
            "payment_method": payment_method,
            "total": discounted_total,
            "cart_items": cart_items,
        })
        pdf_file = io.BytesIO()
        pisa.CreatePDF(io.BytesIO(receipt_html.encode("utf-8")), dest=pdf_file)
        pdf_file.seek(0)
        # Save PDF to Receipt model
        receipt_instance = Receipt.objects.create(
            user=user,
            order_summary=f"Paid {discounted_total} by {payment_method}",
        )
        receipt_instance.pdf.save(f"receipt_{receipt_instance.id}.pdf", pdf_file)
        receipt_instance.save()
    return render(request, "shop/payment_success.html", {
        "user": user,
        "payment_method": payment_method,
        "total": discounted_total,
        "cart_items": cart_items,
    })
