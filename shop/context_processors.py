def cart_context(request):
    """
    Context processor to add cart information to all templates
    """
    cart = request.session.get('cart', {})
    
    # Handle migration from old list format to new dict format
    if isinstance(cart, list):
        cart_count = len(cart)
    else:
        cart_count = sum(cart.values()) if cart else 0
    
    return {
        'cart_count': cart_count
    }
