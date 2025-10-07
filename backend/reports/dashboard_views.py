from __future__ import annotations

from django.db.models import Count, Q
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from matches.models import Match
from notifications.models import Notification
from .models import Report


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics for the current user
    """
    user = request.user
    
    # Get user's reports
    user_reports = Report.objects.filter(reported_by=user)
    total_reports = user_reports.count()
    
    # Get active matches (pending matches for user's reports)
    active_matches = Match.objects.filter(
        Q(lost_report__reported_by=user) | Q(found_report__reported_by=user),
        status=Match.Status.PENDING
    ).count()
    
    # Get resolved items (confirmed matches)
    resolved_items = Match.objects.filter(
        Q(lost_report__reported_by=user) | Q(found_report__reported_by=user),
        status=Match.Status.CONFIRMED
    ).count()
    
    # Get unread notifications
    unread_notifications = Notification.objects.filter(
        user=user,
        is_read=False
    ).count()
    
    return Response({
        'total_reports': total_reports,
        'active_matches': active_matches,
        'resolved_items': resolved_items,
        'notifications': unread_notifications
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_reports(request):
    """
    Get current user's reports
    """
    user = request.user
    reports = Report.objects.filter(reported_by=user).order_by('-created_at')
    
    reports_data = []
    for report in reports:
        reports_data.append({
            'id': report.id,
            'title': report.title,
            'description': report.description,
            'report_type': report.report_type,
            'status': report.status,
            'category': report.category.name,
            'location': report.location,
            'date_lost_found': report.date_lost_found.isoformat(),
            'created_at': report.created_at.isoformat(),
            'image': report.image.url if report.image else None
        })
    
    return Response({
        'results': reports_data,
        'count': len(reports_data)
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_matches(request):
    """
    Get matches for current user's reports
    """
    user = request.user
    matches = Match.objects.filter(
        Q(lost_report__reported_by=user) | Q(found_report__reported_by=user)
    ).order_by('-created_at')
    
    matches_data = []
    for match in matches:
        # Determine if user owns the lost or found report
        user_report = match.lost_report if match.lost_report.reported_by == user else match.found_report
        other_report = match.found_report if match.lost_report.reported_by == user else match.lost_report
        
        matches_data.append({
            'id': match.id,
            'confidence_score': match.confidence_score,
            'status': match.status,
            'created_at': match.created_at.isoformat(),
            'resolved_at': match.resolved_at.isoformat() if match.resolved_at else None,
            'user_report': {
                'id': user_report.id,
                'title': user_report.title,
                'report_type': user_report.report_type,
                'image': user_report.image.url if user_report.image else None
            },
            'matched_report': {
                'id': other_report.id,
                'title': other_report.title,
                'report_type': other_report.report_type,
                'reported_by': other_report.reported_by.username,
                'image': other_report.image.url if other_report.image else None
            }
        })
    
    return Response({
        'results': matches_data,
        'count': len(matches_data)
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_notifications(request):
    """
    Get notifications for current user
    """
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    
    notifications_data = []
    for notification in notifications:
        notifications_data.append({
            'id': notification.id,
            'message': notification.message,
            'is_read': notification.is_read,
            'created_at': notification.created_at.isoformat(),
            'related_match_id': notification.related_match.id if notification.related_match else None
        })
    
    return Response({
        'results': notifications_data,
        'count': len(notifications_data)
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, notification_id):
    """
    Mark a notification as read
    """
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return Response({'success': True})
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=404)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def confirm_match(request, match_id):
    """
    Confirm a match
    """
    try:
        match = Match.objects.get(
            id=match_id,
            status=Match.Status.PENDING
        )
        
        # Check if user owns one of the reports in the match
        user = request.user
        if (match.lost_report.reported_by != user and 
            match.found_report.reported_by != user):
            return Response({'error': 'Not authorized'}, status=403)
        
        match.status = Match.Status.CONFIRMED
        match.save()
        
        # Update report statuses
        match.lost_report.status = Report.Status.MATCHED
        match.found_report.status = Report.Status.MATCHED
        match.lost_report.save()
        match.found_report.save()
        
        return Response({'success': True})
    except Match.DoesNotExist:
        return Response({'error': 'Match not found'}, status=404)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reject_match(request, match_id):
    """
    Reject a match
    """
    try:
        match = Match.objects.get(
            id=match_id,
            status=Match.Status.PENDING
        )
        
        # Check if user owns one of the reports in the match
        user = request.user
        if (match.lost_report.reported_by != user and 
            match.found_report.reported_by != user):
            return Response({'error': 'Not authorized'}, status=403)
        
        match.status = Match.Status.REJECTED
        match.save()
        
        return Response({'success': True})
    except Match.DoesNotExist:
        return Response({'error': 'Match not found'}, status=404)
