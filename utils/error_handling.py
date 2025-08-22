import logging
import traceback
import functools
from datetime import datetime
import streamlit as st

# Konfiguracja logowania
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('zen_degen')

class AppError(Exception):
    """Base exception class for application errors"""
    def __init__(self, message, error_type="error"):
        self.message = message
        self.error_type = error_type
        super().__init__(self.message)

def safe_notification(message, notification_type="info"):
    """
    Bezpieczne wyświetlanie powiadomień - fallback na Streamlit jeśli utils.notifications nie działa
    """
    try:
        from utils.notifications import show_notification
        show_notification(message, notification_type)
    except ImportError:
        # Fallback na standardowe Streamlit
        if notification_type == "error":
            st.error(message)
        elif notification_type == "warning":
            st.warning(message)
        elif notification_type == "success":
            st.success(message)
        else:
            st.info(message)

def handle_error(func):
    """Decorator for handling errors in functions"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AppError as e:
            # Pokaż użytkownikowi przyjazny komunikat
            safe_notification(e.message, e.error_type)
            # Zaloguj błąd
            logger.error(f"AppError in {func.__name__}: {e.message}")
        except Exception as e:
            # Pokaż użytkownikowi ogólny komunikat
            error_msg = f"Wystąpił błąd w funkcji {func.__name__}. Spróbuj ponownie później."
            safe_notification(error_msg, "error")
            
            # Zaloguj szczegółowy błąd
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            
            # W trybie dev wyświetl szczegóły błędu
            if st.session_state.get('dev_mode', False):
                st.exception(e)
        return None
    return wrapper

def safe_execute(func, fallback_value=None, error_message=None):
    """
    Bezpieczne wykonanie funkcji z fallback value
    
    Args:
        func: Funkcja do wykonania
        fallback_value: Wartość zwracana w przypadku błędu
        error_message: Niestandardowy komunikat błędu
    """
    try:
        return func()
    except Exception as e:
        if error_message:
            safe_notification(error_message, "warning")
        else:
            safe_notification(f"Nie udało się wykonać operacji: {str(e)}", "warning")
        
        logger.error(f"Error in safe_execute: {str(e)}")
        return fallback_value

def log_action(action_type):
    """Decorator for logging user actions"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            username = st.session_state.get('username', 'anonymous')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            logger.info(
                f"Action: {action_type} | User: {username} | "
                f"Function: {func.__name__} | Time: {timestamp}"
            )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def validate_user_input(**validators):
    """
    Decorator for validating user input
    Example usage:
    @validate_user_input(
        username=lambda x: len(x) >= 3,
        password=lambda x: len(x) >= 6
    )
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for field, validator in validators.items():
                if field in kwargs:
                    value = kwargs[field]
                    if not validator(value):
                        raise AppError(
                            f"Nieprawidłowa wartość dla pola {field}",
                            "warning"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator

class ErrorBoundary:
    """Context manager for handling errors in specific sections of code"""
    def __init__(self, section_name, show_error=True):
        self.section_name = section_name
        self.show_error = show_error

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            if self.show_error:
                safe_notification(
                    f"Błąd w sekcji {self.section_name}. Spróbuj ponownie.",
                    "error"
                )
            logger.error(
                f"Error in section {self.section_name}: "
                f"{exc_type.__name__}: {str(exc_value)}"
            )
            return True  # Obsłuż błąd
        return False