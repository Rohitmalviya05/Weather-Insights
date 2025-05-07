from datetime import datetime, timedelta
import logging

from app import db
from models import PageVisit
from sqlalchemy import func, desc

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def track_visit(request, page_name):
    """Track a page visit with device and browser info"""
    try:
        user_id = None
        if hasattr(request, 'user') and request.user and request.user.is_authenticated:
            user_id = request.user.id

        user_agent = request.headers.get('User-Agent', '')
        ip_address = request.remote_addr


        visit = PageVisit(
            user_id=user_id,
            page_name=page_name,
            ip_address=ip_address,
            user_agent=user_agent
        )

        db.session.add(visit)
        db.session.commit()

        logger.debug(f"Tracked visit to {page_name}")
    except Exception as e:
        # Log error but don't interrupt normal flow
        logger.error(f"Error tracking visit: {str(e)}")
        db.session.rollback()


def get_visitor_stats(days=30):
    """
    Get various visitor statistics for the analytics dashboard

    Args:
        days: Number of days to include in the stats

    Returns:
        dict: Dictionary with various visitor statistics
    """
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Get total visits in period
        total_visits = db.session.query(PageVisit).filter(
            PageVisit.visit_time >= start_date
        ).count()

        # Get unique visitors (by IP)
        unique_visitors = db.session.query(
            PageVisit.ip_address
        ).filter(
            PageVisit.visit_time >= start_date
        ).distinct().count()

        # Get visits by page
        page_visits = db.session.query(
            PageVisit.page_name,
            func.count(PageVisit.id).label('count')
        ).filter(
            PageVisit.visit_time >= start_date
        ).group_by(PageVisit.page_name).order_by(desc('count')).all()

        page_visit_data = [{'page': page, 'count': count} for page, count in page_visits]

        # Get visits by date
        date_visits = db.session.query(
            func.date(PageVisit.visit_time).label('date'),
            func.count(PageVisit.id).label('count')
        ).filter(
            PageVisit.visit_time >= start_date
        ).group_by('date').order_by('date').all()

        date_visit_data = [{'date': date.strftime('%Y-%m-%d'), 'count': count} 
                           for date, count in date_visits]

        # Get user agent stats
        # This is a simple mobile/desktop detection - could be more sophisticated
        mobile_count = db.session.query(PageVisit).filter(
            PageVisit.visit_time >= start_date,
            PageVisit.user_agent.ilike('%mobile%')
        ).count()

        desktop_count = total_visits - mobile_count

        device_data = [
            {'device': 'Mobile', 'count': mobile_count},
            {'device': 'Desktop', 'count': desktop_count}
        ]

        # Compile all stats
        return {
            'total_visits': total_visits,
            'unique_visitors': unique_visitors,
            'page_visits': page_visit_data,
            'date_visits': date_visit_data,
            'devices': device_data
        }
    except Exception as e:
        logger.error(f"Error getting visitor stats: {str(e)}")
        return {
            'error': str(e),
            'total_visits': 0,
            'unique_visitors': 0,
            'page_visits': [],
            'date_visits': [],
            'devices': []
        }