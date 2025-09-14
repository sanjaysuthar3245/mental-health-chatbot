"""
Mood Tracking Routes - Handles mood tracking and analytics
"""

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from src.db.models import MoodEntry, db
from datetime import datetime, timedelta
import json

mood_tracking_bp = Blueprint('mood_tracking', __name__)

@mood_tracking_bp.route('/')
@login_required
def index():
    """Mood tracking dashboard"""
    return render_template('mood_tracking.html')

@mood_tracking_bp.route('/api/entry', methods=['POST'])
@login_required
def create_mood_entry():
    """Create a new mood entry"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['mood_score', 'energy_level', 'stress_level']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create mood entry
    mood_entry = MoodEntry(
        user_id=current_user.id,
        mood_score=data['mood_score'],
        energy_level=data['energy_level'],
        stress_level=data['stress_level'],
        sleep_hours=data.get('sleep_hours'),
        physical_activity=data.get('physical_activity'),
        social_activity=data.get('social_activity'),
        notes=data.get('notes', ''),
        tags=data.get('tags', [])
    )
    
    db.session.add(mood_entry)
    db.session.commit()
    
    return jsonify({
        'message': 'Mood entry created successfully',
        'entry_id': mood_entry.id
    })

@mood_tracking_bp.route('/api/entry/<int:entry_id>', methods=['PUT'])
@login_required
def update_mood_entry(entry_id):
    """Update an existing mood entry"""
    mood_entry = MoodEntry.query.filter_by(id=entry_id, user_id=current_user.id).first()
    if not mood_entry:
        return jsonify({'error': 'Mood entry not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    if 'mood_score' in data:
        mood_entry.mood_score = data['mood_score']
    if 'energy_level' in data:
        mood_entry.energy_level = data['energy_level']
    if 'stress_level' in data:
        mood_entry.stress_level = data['stress_level']
    if 'sleep_hours' in data:
        mood_entry.sleep_hours = data['sleep_hours']
    if 'physical_activity' in data:
        mood_entry.physical_activity = data['physical_activity']
    if 'social_activity' in data:
        mood_entry.social_activity = data['social_activity']
    if 'notes' in data:
        mood_entry.notes = data['notes']
    if 'tags' in data:
        mood_entry.tags = data['tags']
    
    mood_entry.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({'message': 'Mood entry updated successfully'})

@mood_tracking_bp.route('/api/entry/<int:entry_id>', methods=['DELETE'])
@login_required
def delete_mood_entry(entry_id):
    """Delete a mood entry"""
    mood_entry = MoodEntry.query.filter_by(id=entry_id, user_id=current_user.id).first()
    if not mood_entry:
        return jsonify({'error': 'Mood entry not found'}), 404
    
    db.session.delete(mood_entry)
    db.session.commit()
    
    return jsonify({'message': 'Mood entry deleted successfully'})

@mood_tracking_bp.route('/api/entries')
@login_required
def get_mood_entries():
    """Get mood entries for the current user"""
    # Get query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', 30, type=int)
    
    # Build query
    query = MoodEntry.query.filter_by(user_id=current_user.id)
    
    if start_date:
        query = query.filter(MoodEntry.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(MoodEntry.created_at <= datetime.fromisoformat(end_date))
    
    # Order by date and limit
    entries = query.order_by(MoodEntry.created_at.desc()).limit(limit).all()
    
    # Convert to JSON
    entries_data = []
    for entry in entries:
        entries_data.append({
            'id': entry.id,
            'mood_score': entry.mood_score,
            'energy_level': entry.energy_level,
            'stress_level': entry.stress_level,
            'sleep_hours': entry.sleep_hours,
            'physical_activity': entry.physical_activity,
            'social_activity': entry.social_activity,
            'notes': entry.notes,
            'tags': entry.tags,
            'created_at': entry.created_at.isoformat(),
            'updated_at': entry.updated_at.isoformat() if entry.updated_at else None
        })
    
    return jsonify({
        'entries': entries_data,
        'total_count': len(entries_data)
    })

@mood_tracking_bp.route('/api/analytics')
@login_required
def get_mood_analytics():
    """Get mood analytics and insights"""
    # Get date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)  # Last 30 days
    
    # Get mood entries
    entries = MoodEntry.query.filter(
        MoodEntry.user_id == current_user.id,
        MoodEntry.created_at >= start_date,
        MoodEntry.created_at <= end_date
    ).order_by(MoodEntry.created_at).all()
    
    if not entries:
        return jsonify({
            'message': 'No mood entries found for the selected period',
            'analytics': {}
        })
    
    # Calculate analytics
    mood_scores = [entry.mood_score for entry in entries]
    energy_levels = [entry.energy_level for entry in entries]
    stress_levels = [entry.stress_level for entry in entries]
    
    analytics = {
        'period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'total_entries': len(entries)
        },
        'mood': {
            'average': sum(mood_scores) / len(mood_scores),
            'min': min(mood_scores),
            'max': max(mood_scores),
            'trend': _calculate_trend(mood_scores)
        },
        'energy': {
            'average': sum(energy_levels) / len(energy_levels),
            'min': min(energy_levels),
            'max': max(energy_levels),
            'trend': _calculate_trend(energy_levels)
        },
        'stress': {
            'average': sum(stress_levels) / len(stress_levels),
            'min': min(stress_levels),
            'max': max(stress_levels),
            'trend': _calculate_trend(stress_levels)
        },
        'insights': _generate_insights(entries),
        'recommendations': _generate_mood_recommendations(entries)
    }
    
    return jsonify({'analytics': analytics})

@mood_tracking_bp.route('/api/export')
@login_required
def export_mood_data():
    """Export mood data as CSV"""
    import csv
    import io
    from flask import Response
    
    # Get mood entries
    entries = MoodEntry.query.filter_by(user_id=current_user.id).order_by(MoodEntry.created_at).all()
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Date', 'Mood Score', 'Energy Level', 'Stress Level', 
        'Sleep Hours', 'Physical Activity', 'Social Activity', 'Notes', 'Tags'
    ])
    
    # Write data
    for entry in entries:
        writer.writerow([
            entry.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            entry.mood_score,
            entry.energy_level,
            entry.stress_level,
            entry.sleep_hours or '',
            entry.physical_activity or '',
            entry.social_activity or '',
            entry.notes or '',
            ', '.join(entry.tags) if entry.tags else ''
        ])
    
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=mood_data.csv'}
    )

def _calculate_trend(values):
    """Calculate trend for a series of values"""
    if len(values) < 2:
        return 'stable'
    
    # Simple linear trend calculation
    n = len(values)
    x = list(range(n))
    y = values
    
    # Calculate slope
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    
    numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
    
    if denominator == 0:
        return 'stable'
    
    slope = numerator / denominator
    
    if slope > 0.1:
        return 'improving'
    elif slope < -0.1:
        return 'declining'
    else:
        return 'stable'

def _generate_insights(entries):
    """Generate insights from mood entries"""
    insights = []
    
    if len(entries) < 7:
        return ['Need more data to generate insights']
    
    # Mood patterns
    mood_scores = [entry.mood_score for entry in entries]
    avg_mood = sum(mood_scores) / len(mood_scores)
    
    if avg_mood > 7:
        insights.append('Your mood has been consistently positive recently')
    elif avg_mood < 4:
        insights.append('Your mood has been consistently low recently')
    else:
        insights.append('Your mood has been relatively stable recently')
    
    # Sleep correlation
    sleep_entries = [entry for entry in entries if entry.sleep_hours is not None]
    if sleep_entries:
        sleep_mood_correlation = _calculate_correlation(
            [entry.sleep_hours for entry in sleep_entries],
            [entry.mood_score for entry in sleep_entries]
        )
        
        if sleep_mood_correlation > 0.3:
            insights.append('Better sleep appears to correlate with better mood')
        elif sleep_mood_correlation < -0.3:
            insights.append('Poor sleep appears to correlate with lower mood')
    
    # Activity correlation
    activity_entries = [entry for entry in entries if entry.physical_activity is not None]
    if activity_entries:
        activity_mood_correlation = _calculate_correlation(
            [entry.physical_activity for entry in activity_entries],
            [entry.mood_score for entry in activity_entries]
        )
        
        if activity_mood_correlation > 0.3:
            insights.append('Physical activity appears to improve your mood')
        elif activity_mood_correlation < -0.3:
            insights.append('Physical activity appears to correlate with lower mood')
    
    return insights

def _generate_mood_recommendations(entries):
    """Generate recommendations based on mood data"""
    recommendations = []
    
    if len(entries) < 7:
        return ['Continue tracking to get personalized recommendations']
    
    # Analyze patterns
    mood_scores = [entry.mood_score for entry in entries]
    stress_levels = [entry.stress_level for entry in entries]
    
    avg_mood = sum(mood_scores) / len(mood_scores)
    avg_stress = sum(stress_levels) / len(stress_levels)
    
    if avg_mood < 5:
        recommendations.append('Consider talking to a mental health professional')
        recommendations.append('Try engaging in activities you used to enjoy')
    
    if avg_stress > 7:
        recommendations.append('Practice stress management techniques like deep breathing')
        recommendations.append('Consider taking regular breaks throughout the day')
    
    # Sleep recommendations
    sleep_entries = [entry for entry in entries if entry.sleep_hours is not None]
    if sleep_entries:
        avg_sleep = sum(entry.sleep_hours for entry in sleep_entries) / len(sleep_entries)
        if avg_sleep < 7:
            recommendations.append('Aim for 7-9 hours of sleep per night')
        elif avg_sleep > 9:
            recommendations.append('Consider if oversleeping might be affecting your mood')
    
    return recommendations

def _calculate_correlation(x, y):
    """Calculate correlation coefficient between two lists"""
    if len(x) != len(y) or len(x) < 2:
        return 0
    
    n = len(x)
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    
    numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    x_variance = sum((x[i] - x_mean) ** 2 for i in range(n))
    y_variance = sum((y[i] - y_mean) ** 2 for i in range(n))
    
    if x_variance == 0 or y_variance == 0:
        return 0
    
    return numerator / (x_variance * y_variance) ** 0.5

