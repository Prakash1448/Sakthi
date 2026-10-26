"""
PDF Report Generator with Visual Charts
Generates comprehensive interview reports for candidates with attractive graphs
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os
import tempfile

# Matplotlib for charts
try:
    import matplotlib
    matplotlib.use('Agg')  # Non-GUI backend
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  matplotlib not available. Install with: pip install matplotlib")


def create_score_bar_chart(level_data: dict, output_path: str) -> str:
    """
    Create a bar chart showing scores across different levels.
    
    Args:
        level_data: Dictionary with level names as keys
        output_path: Where to save the chart
    
    Returns:
        Path to the saved chart image
    """
    if not MATPLOTLIB_AVAILABLE:
        return None
    
    levels = []
    scores = []
    
    for level, sessions in level_data.items():
        if sessions:
            latest = sessions[0]
            levels.append(level.replace("Level ", "L").replace(" - ", "\n"))  # Shorter labels
            scores.append(latest.get('total_score', 0))
    
    if not levels:
        return None
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Color gradient from red to green based on score
    colors_list = []
    for score in scores:
        if score >= 7:
            colors_list.append('#10b981')  # Green
        elif score >= 5:
            colors_list.append('#f59e0b')  # Orange
        else:
            colors_list.append('#ef4444')  # Red
    
    bars = ax.bar(levels, scores, color=colors_list, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{score:.1f}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_ylabel('Score (out of 10)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Interview Levels', fontsize=12, fontweight='bold')
    ax.set_title('Performance Across Interview Levels', fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 10.5)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_path


def create_completion_pie_chart(stats: dict, output_path: str) -> str:
    """
    Create a pie chart showing answered vs unanswered questions.
    
    Args:
        stats: Statistics dictionary
        output_path: Where to save the chart
    
    Returns:
        Path to the saved chart image
    """
    if not MATPLOTLIB_AVAILABLE:
        return None
    
    answered = stats.get("total_answered", 0)
    total = stats.get("total_questions", 1)
    unanswered = total - answered
    
    if total == 0:
        return None
    
    # Create figure
    fig, ax = plt.subplots(figsize=(7, 7))
    
    sizes = [answered, unanswered]
    labels = [f'Answered\n{answered}', f'Unanswered\n{unanswered}']
    colors_list = ['#10b981', '#e5e7eb']
    explode = (0.05, 0)
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                        colors=colors_list, explode=explode,
                                        shadow=True, startangle=90,
                                        textprops={'fontsize': 12, 'fontweight': 'bold'})
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
        autotext.set_fontweight('bold')
    
    ax.set_title('Question Completion Rate', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_path


def create_radar_chart(level_data: dict, output_path: str) -> str:
    """
    Create a radar/spider chart showing performance across levels.
    
    Args:
        level_data: Dictionary with level names as keys
        output_path: Where to save the chart
    
    Returns:
        Path to the saved chart image
    """
    if not MATPLOTLIB_AVAILABLE:
        return None
    
    levels = []
    scores = []
    
    for level, sessions in level_data.items():
        if sessions:
            latest = sessions[0]
            # Shorten level names
            short_name = level.replace("Level ", "L").replace(" - ", ":\n")
            levels.append(short_name)
            scores.append(latest.get('total_score', 0))
    
    if len(levels) < 3:
        return None  # Radar chart needs at least 3 points
    
    # Number of variables
    num_vars = len(levels)
    
    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    # Close the plot
    scores += scores[:1]
    angles += angles[:1]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    
    # Plot data
    ax.plot(angles, scores, 'o-', linewidth=2, color='#3b82f6', label='Your Score')
    ax.fill(angles, scores, alpha=0.25, color='#3b82f6')
    
    # Plot maximum (10)
    max_scores = [10] * (num_vars + 1)
    ax.plot(angles, max_scores, '--', linewidth=1, color='#10b981', alpha=0.5, label='Maximum')
    
    # Fix axis to go from 0 to 10
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=10)
    
    # Set category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(levels, fontsize=10, fontweight='bold')
    
    ax.set_title('Multi-Level Performance Analysis', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_path


def create_performance_gauge(avg_score: float, output_path: str) -> str:
    """
    Create a gauge/speedometer chart showing overall performance.
    
    Args:
        avg_score: Average score (0-10)
        output_path: Where to save the chart
    
    Returns:
        Path to the saved chart image
    """
    if not MATPLOTLIB_AVAILABLE:
        return None
    
    fig, ax = plt.subplots(figsize=(8, 4), subplot_kw=dict(projection='polar'))
    
    # Gauge parameters
    theta = np.linspace(0, np.pi, 100)
    
    # Background segments
    segments = [
        (0, np.pi/3, '#ef4444', 'Needs Improvement'),
        (np.pi/3, 2*np.pi/3, '#f59e0b', 'Good'),
        (2*np.pi/3, np.pi, '#10b981', 'Excellent')
    ]
    
    for start, end, color, label in segments:
        t = np.linspace(start, end, 50)
        ax.fill_between(t, 0, 1, alpha=0.3, color=color)
    
    # Needle position
    needle_angle = (avg_score / 10) * np.pi
    ax.plot([needle_angle, needle_angle], [0, 0.9], 'k-', linewidth=4)
    ax.plot(needle_angle, 0.9, 'ko', markersize=15)
    
    # Score text
    ax.text(np.pi/2, 0.5, f'{avg_score:.1f}/10', 
            ha='center', va='center', fontsize=24, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='black', linewidth=2))
    
    ax.set_ylim(0, 1)
    ax.set_xlim(0, np.pi)
    ax.set_yticks([])
    ax.set_xticks([0, np.pi/3, 2*np.pi/3, np.pi])
    ax.set_xticklabels(['0', '3.3', '6.7', '10'], fontsize=10)
    ax.spines['polar'].set_visible(False)
    ax.grid(False)
    ax.set_title('Overall Performance Score', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_path


def generate_user_report_pdf(report_data: dict, output_path: str = None) -> str:
    """
    Generate comprehensive PDF report for a user across all levels.
    
    Args:
        report_data: Complete user data from database.get_user_report_data()
        output_path: Optional output path. If None, creates in reports/ folder
    
    Returns:
        Path to generated PDF file
    """
    user = report_data["user"]
    sessions = report_data["sessions"]
    level_data = report_data["level_data"]
    stats = report_data["statistics"]
    
    # Create reports directory if it doesn't exist
    if output_path is None:
        os.makedirs("reports", exist_ok=True)
        output_path = f"reports/{user['username']}_full_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    # Create PDF document
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    elements.append(Paragraph("AI Interview Platform", title_style))
    elements.append(Paragraph("Comprehensive Interview Report", styles['Heading2']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Candidate Information
    elements.append(Paragraph("Candidate Information", heading_style))
    
    candidate_data = [
        ["Candidate Name:", user["username"]],
        ["Domain:", user.get("domain", "N/A")],
        ["Total Sessions:", str(stats["total_sessions"])],
        ["Completed Levels:", ", ".join(user.get("completed_levels", [])) or "None"],
        ["Average Score:", f"{stats['average_score']:.2f}/10"],
        ["Report Generated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    ]
    
    candidate_table = Table(candidate_data, colWidths=[2*inch, 4*inch])
    candidate_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(candidate_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Overall Statistics
    elements.append(Paragraph("Overall Statistics", heading_style))
    
    stats_data = [
        ["Total Questions Asked:", str(stats["total_questions"])],
        ["Total Questions Answered:", str(stats["total_answered"])],
        ["Completion Rate:", f"{stats['completion_rate']:.2f}%"],
        ["Proctoring Warnings:", str(stats["total_warnings"])],
    ]
    
    stats_table = Table(stats_data, colWidths=[2.5*inch, 3.5*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#dbeafe')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Level-wise Performance
    elements.append(Paragraph("Performance by Level", heading_style))
    
    for level, level_sessions in level_data.items():
        latest = level_sessions[0]  # Most recent session
        
        level_info = f"<b>{level}</b> (Attempted: {len(level_sessions)} time(s))"
        elements.append(Paragraph(level_info, styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        
        level_perf_data = [
            ["Status:", latest["status"].title()],
            ["Score:", f"{latest.get('total_score', 0):.2f}/10"],
            ["Percentage:", f"{latest.get('percentage', 0):.2f}%"],
            ["Questions Answered:", f"{len([a for a in latest.get('candidate_answers', []) if a])}/{len(latest['questions'])}"],
            ["Proctoring Warnings:", str(latest.get("proctoring_warnings", 0))],
            ["Date:", latest["started_at"].strftime("%Y-%m-%d %H:%M")]
        ]
        
        level_table = Table(level_perf_data, colWidths=[2*inch, 4*inch])
        level_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f9ff')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(level_table)
        elements.append(Spacer(1, 0.2*inch))
    
    # Page break before detailed answers
    elements.append(PageBreak())
    
    # Detailed Q&A for each level
    for level, level_sessions in level_data.items():
        latest = level_sessions[0]
        
        elements.append(Paragraph(f"Detailed Answers - {level}", heading_style))
        elements.append(Spacer(1, 0.1*inch))
        
        questions = latest.get("questions", [])
        answers = latest.get("candidate_answers", [])
        evaluations = latest.get("evaluations", [])
        
        for idx, question in enumerate(questions):
            # Question
            q_text = f"<b>Q{idx+1}:</b> {question}"
            elements.append(Paragraph(q_text, styles['Normal']))
            elements.append(Spacer(1, 0.05*inch))
            
            # Answer
            answer = answers[idx] if idx < len(answers) and answers[idx] else "Not answered"
            a_text = f"<b>Answer:</b> {answer[:200]}{'...' if len(answer) > 200 else ''}"
            elements.append(Paragraph(a_text, styles['Normal']))
            elements.append(Spacer(1, 0.05*inch))
            
            # Evaluation
            if idx < len(evaluations) and evaluations[idx]:
                eval_data = evaluations[idx]
                score = eval_data.get("score", 0)
                feedback = eval_data.get("feedback", "No feedback")
                
                eval_text = f"<b>Score:</b> {score}/10 | <b>Feedback:</b> {feedback[:150]}{'...' if len(feedback) > 150 else ''}"
                elements.append(Paragraph(eval_text, styles['Normal']))
            else:
                elements.append(Paragraph("<b>Not evaluated yet</b>", styles['Normal']))
            
            elements.append(Spacer(1, 0.15*inch))
        
        elements.append(PageBreak())
    
    # Final Summary
    elements.append(Paragraph("Summary & Recommendations", heading_style))
    
    # Generate recommendations based on performance
    avg_score = stats["average_score"]
    completion = stats["completion_rate"]
    
    if avg_score >= 7 and completion >= 80:
        recommendation = "Excellent performance! The candidate demonstrates strong knowledge and skills."
    elif avg_score >= 5 and completion >= 60:
        recommendation = "Good performance. The candidate shows promise with room for improvement."
    elif avg_score >= 3:
        recommendation = "Moderate performance. Additional training and practice recommended."
    else:
        recommendation = "Needs significant improvement. Consider focused learning and re-evaluation."
    
    elements.append(Paragraph(recommendation, styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Footer
    footer_text = f"<i>Report generated by AI Interview Platform | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"
    elements.append(Paragraph(footer_text, styles['Italic']))
    
    # Build PDF
    doc.build(elements)
    
    return output_path


def generate_level_report_pdf(report_data: dict, output_path: str = None) -> str:
    """
    Generate PDF report for a single level (even if incomplete).
    
    Args:
        report_data: Level session data from database.get_level_report_data()
        output_path: Optional output path
    
    Returns:
        Path to generated PDF file
    """
    username = report_data["username"]
    level = report_data["level"]
    session = report_data["session"]
    
    # Create reports directory
    if output_path is None:
        os.makedirs("reports", exist_ok=True)
        output_path = f"reports/{username}_{level.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    # Create PDF
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=10,
        spaceBefore=10
    )
    
    # Title
    elements.append(Paragraph("AI Interview Report", title_style))
    elements.append(Paragraph(level, styles['Heading2']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Session Info
    info_data = [
        ["Candidate:", username],
        ["Level:", level],
        ["Status:", session["status"].title()],
        ["Started:", session["started_at"].strftime("%Y-%m-%d %H:%M:%S")],
        ["Score:", f"{session.get('total_score', 0):.2f}/10"],
        ["Percentage:", f"{session.get('percentage', 0):.2f}%"],
        ["Warnings:", str(session.get("proctoring_warnings", 0))]
    ]
    
    info_table = Table(info_data, colWidths=[1.5*inch, 4.5*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#dbeafe')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Questions and Answers
    elements.append(Paragraph("Questions & Answers", heading_style))
    
    questions = session.get("questions", [])
    answers = session.get("candidate_answers", [])
    evaluations = session.get("evaluations", [])
    
    for idx, question in enumerate(questions):
        # Question
        elements.append(Paragraph(f"<b>Question {idx+1}:</b> {question}", styles['Normal']))
        elements.append(Spacer(1, 0.05*inch))
        
        # Answer
        answer = answers[idx] if idx < len(answers) and answers[idx] else "Not answered"
        elements.append(Paragraph(f"<b>Answer:</b> {answer}", styles['Normal']))
        elements.append(Spacer(1, 0.05*inch))
        
        # Evaluation
        if idx < len(evaluations) and evaluations[idx]:
            eval_data = evaluations[idx]
            score = eval_data.get("score", 0)
            feedback = eval_data.get("feedback", "No feedback")
            
            elements.append(Paragraph(f"<b>Score:</b> {score}/10", styles['Normal']))
            elements.append(Paragraph(f"<b>Feedback:</b> {feedback}", styles['Normal']))
        else:
            elements.append(Paragraph("<b>Status:</b> Not evaluated", styles['Normal']))
        
        elements.append(Spacer(1, 0.2*inch))
    
    # Footer
    footer = f"<i>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(footer, styles['Italic']))
    
    # Build PDF
    doc.build(elements)
    
    return output_path


# ============================================================================
# Testing
# ============================================================================

if __name__ == "__main__":
    print("="*60)
    print("PDF Report Generator Test")
    print("="*60)
    
    # Create dummy data for testing
    test_user_data = {
        "user": {
            "username": "Test Candidate",
            "domain": "Python",
            "completed_levels": ["Level 1 - Basic Fundamentals"],
            "average_score": 7.5
        },
        "sessions": [],
        "level_data": {
            "Level 1 - Basic Fundamentals": [{
                "questions": ["Q1", "Q2"],
                "candidate_answers": ["A1", "A2"],
                "evaluations": [{"score": 7, "feedback": "Good"}, {"score": 8, "feedback": "Excellent"}],
                "total_score": 7.5,
                "percentage": 75.0,
                "status": "completed",
                "proctoring_warnings": 2,
                "started_at": datetime.now()
            }]
        },
        "statistics": {
            "total_sessions": 1,
            "total_questions": 2,
            "total_answered": 2,
            "average_score": 7.5,
            "total_warnings": 2,
            "completion_rate": 100.0
        }
    }
    
    # Generate test report
    try:
        pdf_path = generate_user_report_pdf(test_user_data, "test_report.pdf")
        print(f"\n✅ PDF generated successfully: {pdf_path}")
    except Exception as e:
        print(f"\n❌ PDF generation failed: {e}")
