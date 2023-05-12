from flask import flash, Markup

def flash_message(message, category):
    """Helper function to flash a Bootstrap-styled message"""
    category_map = {
        'info': 'primary',
        'success': 'success',
        'warning': 'warning',
        'error': 'danger'
    }
    flash(Markup(f'<div class="alert alert-{category_map.get(category, "info")}">{message}</div>'), category)
