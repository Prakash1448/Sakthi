"""
Enhanced PDF Report Generator with Visual Charts
Generates comprehensive interview reports for candidates with attractive graphs
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
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
    print("⚠️  matplotlib not available. Install with: pip install matplotlib numpy")


def create_score_bar_chart(level_data: dict, output_path: str) -> str:
    """Create a bar chart showing scores across different levels."""
    if not MATPLOTLIB_AVAILABLE or not level_data:
        return None
    
    levels = []
    scores = []
    
    for level, sessions in level_data.items():
        if sessions:
            latest = sessions[0]
            # Shorten level names for display
            short_name = level.replace("Level ", "L").replace(" - ", "\n")
            levels.append(short_name)
            scores.append(latest.get('total_score', 0))
    
    if not levels:
        return None
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Color gradient based on score
    colors_list = []
    for score in scores:
        if score >= 7:
            colors_list.append('#10b981')  # Green
        elif score >= 5:
            colors_list.append('#f59e0b')  # Orange
        else:
            colors_list.append('#ef4444')  # Red
    
    bars = ax.bar(levels, scores, color=colors_list, edgecolor='black', linewidth=1.5, alpha=0.8)
    
    # Add value labels on bars
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                f'{score:.1f}',
                ha='center', va='bottom', fontsize=13, fontweight='bold')
    
    ax.set_ylabel('Score (out of 10)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Interview Levels', fontsize=13, fontweight='bold')
    ax.set_title('Performance Across Interview Levels', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output_path


def create_completion_pie_chart(stats: dict, output_path: str) -> str:
    """Create a pie chart showing answered vs unanswered questions."""
    if not MATPLOTLIB_AVAILABLE:
        return None
    
    answered = stats.get("total_answered", 0)
    total = stats.get("total_questions", 1)
    unanswered = max(0, total - answered)
    
    if total == 0:
        return None
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8))
    
    sizes = [answered, unanswered]
    labels = [f'Answered\n{answered} questions', f'Unanswered\n{unanswered} questions']
    colors_list = ['#10b981', '#e5e7eb']
    explode = (0.05, 0)
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                        colors=colors_list, explode=explode,
                                        shadow=True, startangle=90,
                                        textprops={'fontsize': 12, 'fontweight': 'bold'})
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(16)
        autotext.set_fontweight('bold')
    
    ax.set_title('Question Completion Rate', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output_path


def create_performance_gauge(avg_score: float, output_path: str) -> str:
    """Create a gauge/speedometer chart showing overall performance."""
    if not MATPLOTLIB_AVAILABLE:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 5), subplot_kw=dict(projection='polar'))
    
    # Gauge parameters
    theta = np.linspace(0, np.pi, 100)
    
    # Background segments
    segments = [
        (0, np.pi/3, '#ef4444', 'Needs\nImprovement'),
        (np.pi/3, 2*np.pi/3, '#f59e0b', 'Good'),
        (2*np.pi/3, np.pi, '#10b981', 'Excellent')
    ]
    
    for start, end, color, label in segments:
        t = np.linspace(start, end, 50)
        ax.fill_between(t, 0, 1, alpha=0.4, color=color, label=label)
    
    # Needle position
    needle_angle = (avg_score / 10) * np.pi
    ax.plot([needle_angle, needle_angle], [0, 0.85], 'k-', linewidth=5)
    ax.plot(needle_angle, 0.85, 'ko', markersize=18)
    
    # Score text in center
    ax.text(np.pi/2, 0.3, f'{avg_score:.1f}', 
            ha='center', va='center', fontsize=40, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='black', linewidth=3))
    ax.text(np.pi/2, 0.05, 'out of 10', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    
    ax.set_ylim(0, 1)
    ax.set_xlim(0, np.pi)
    ax.set_yticks([])
    ax.set_xticks([0, np.pi/3, 2*np.pi/3, np.pi])
    ax.set_xticklabels(['0', '3.3', '6.7', '10'], fontsize=11)
    ax.spines['polar'].set_visible(False)
    ax.grid(False)
    ax.set_title('Overall Performance Score', fontsize=16, fontweight='bold', pad=30)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output_path


def create_radar_chart(level_data: dict, output_path: str) -> str:
    """Create a radar/spider chart showing performance across levels."""
    if not MATPLOTLIB_AVAILABLE or not level_data:
        return None
    
    levels = []
    scores = []
    
    for level, sessions in level_data.items():
        if sessions:
            latest = sessions[0]
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
    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(projection='polar'))
    
    # Plot data
    ax.plot(angles, scores, 'o-', linewidth=3, color='#3b82f6', label='Your Score', markersize=8)
    ax.fill(angles, scores, alpha=0.25, color='#3b82f6')
    
    # Plot maximum (10)
    max_scores = [10] * (num_vars + 1)
    ax.plot(angles, max_scores, '--', linewidth=2, color='#10b981', alpha=0.6, label='Maximum (10)')
    
    # Fix axis to go from 0 to 10
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=11)
    
    # Set category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(levels, fontsize=11, fontweight='bold')
    
    ax.set_title('Multi-Level Performance Analysis', fontsize=16, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.15), fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output_path


def generate_enhanced_pdf_report(report_data: dict, output_path: str = None) -> str:
    """
    Generate comprehensive PDF report with charts and graphs.
    
    Args:
        report_data: Complete user data with format:
            {
                "user": {"username": str, "domain": str, ...},
                "sessions": [...],
                "level_data": {level_name: [sessions]},
                "statistics": {"average_score": float, "total_questions": int, ...}
            }
        output_path: Optional output path
    
    Returns:
        Path to generated PDF file
    """
    user = report_data["user"]
    level_data = report_data.get("level_data", {})
    stats = report_data["statistics"]
    
    # Create reports directory
    if output_path is None:
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"reports/{user['username']}_report_{timestamp}.pdf"
    
    # Create temporary directory for charts
    temp_dir = tempfile.mkdtemp()
    chart_paths = {}
    
    # Generate charts
    if MATPLOTLIB_AVAILABLE and level_data:
        try:
            chart_paths['bar'] = create_score_bar_chart(level_data, os.path.join(temp_dir, 'bar.png'))
            chart_paths['pie'] = create_completion_pie_chart(stats, os.path.join(temp_dir, 'pie.png'))
            chart_paths['gauge'] = create_performance_gauge(stats["average_score"], os.path.join(temp_dir, 'gauge.png'))
            
            if len(level_data) >= 3:
                chart_paths['radar'] = create_radar_chart(level_data, os.path.join(temp_dir, 'radar.png'))
        except Exception as e:
            print(f"⚠️  Chart generation error: {e}")
    
    # Create PDF
    doc = SimpleDocTemplate(output_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=28,
                                  textColor=colors.HexColor('#1e40af'), spaceAfter=20,
                                  alignment=TA_CENTER, fontName='Helvetica-Bold')
    
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=16,
                                   textColor=colors.HexColor('#2563eb'), spaceAfter=12,
                                   spaceBefore=15, fontName='Helvetica-Bold')
    
    # ==================== COVER PAGE ====================
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph("🎯 AI INTERVIEW PLATFORM", title_style))
    elements.append(Paragraph("<b>Performance Report</b>", 
                             ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=18,
                                           alignment=TA_CENTER, spaceAfter=30)))
    elements.append(Spacer(1, 0.5*inch))
    
    # Candidate info box
    info_data = [
        ["CANDIDATE:", user["username"].upper()],
        ["DOMAIN:", user.get("domain", "N/A").upper()],
        ["AVERAGE SCORE:", f"{stats['average_score']:.1f}/10"],
    ]
    
    info_table = Table(info_data, colWidths=[2.5*inch, 3.5*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 0.8*inch))
    
    # Gauge chart
    if chart_paths.get('gauge'):
        try:
            gauge_img = Image(chart_paths['gauge'], width=6*inch, height=3*inch)
            elements.append(gauge_img)
        except Exception as e:
            print(f"Error adding gauge: {e}")
    
    elements.append(Spacer(1, 0.5*inch))
    date_text = f"<i>Generated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</i>"
    elements.append(Paragraph(date_text, ParagraphStyle('Date', parent=styles['Normal'],
                                                         alignment=TA_CENTER, fontSize=10)))
    
    elements.append(PageBreak())
    
    # ==================== STATISTICS PAGE ====================
    elements.append(Paragraph("📊 Performance Statistics", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Stats table
    stats_data = [
        ["Total Questions:", str(stats["total_questions"])],
        ["Questions Answered:", str(stats["total_answered"])],
        ["Completion Rate:", f"{stats['completion_rate']:.1f}%"],
        ["Average Score:", f"{stats['average_score']:.2f}/10"],
        ["Total Sessions:", str(stats["total_sessions"])],
        ["Proctoring Warnings:", str(stats["total_warnings"])],
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#dbeafe')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Bar chart
    if chart_paths.get('bar'):
        try:
            elements.append(Paragraph("Level-wise Performance", heading_style))
            bar_img = Image(chart_paths['bar'], width=6.5*inch, height=3.9*inch)
            elements.append(bar_img)
        except Exception as e:
            print(f"Error adding bar chart: {e}")
    
    elements.append(PageBreak())
    
    # ==================== ANALYSIS PAGE ====================
    
    # Pie chart
    if chart_paths.get('pie'):
        try:
            elements.append(Paragraph("Question Completion Analysis", heading_style))
            pie_img = Image(chart_paths['pie'], width=5*inch, height=5*inch)
            elements.append(pie_img)
            elements.append(Spacer(1, 0.3*inch))
        except Exception as e:
            print(f"Error adding pie chart: {e}")
    
    # Radar chart (if 3+ levels)
    if chart_paths.get('radar'):
        try:
            elements.append(Paragraph("Multi-Dimensional Performance", heading_style))
            radar_img = Image(chart_paths['radar'], width=5.5*inch, height=5.5*inch)
            elements.append(radar_img)
        except Exception as e:
            print(f"Error adding radar chart: {e}")
    
    elements.append(PageBreak())
    
    # ==================== LEVEL DETAILS ====================
    elements.append(Paragraph("📋 Level-wise Details", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    for level, sessions in level_data.items():
        if sessions:
            latest = sessions[0]
            
            # Level header
            level_header = f"<b>{level}</b>"
            elements.append(Paragraph(level_header, styles['Heading3']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Level stats
            level_stats = [
                ["Status:", latest["status"].title()],
                ["Score:", f"{latest.get('total_score', 0):.2f}/10"],
                ["Percentage:", f"{latest.get('percentage', 0):.1f}%"],
                ["Questions:", f"{len([a for a in latest.get('candidate_answers', []) if a])}/{len(latest['questions'])}"],
                ["Warnings:", str(latest.get("proctoring_warnings", 0))],
            ]
            
            level_table = Table(level_stats, colWidths=[2*inch, 4*inch])
            level_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f9ff')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            elements.append(level_table)
            elements.append(Spacer(1, 0.3*inch))
    
    # ==================== RECOMMENDATIONS ====================
    elements.append(Paragraph("💡 Recommendations", heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    avg_score = stats["average_score"]
    completion = stats["completion_rate"]
    
    if avg_score >= 7 and completion >= 80:
        recommendation = "✅ <b>Excellent performance!</b> The candidate demonstrates strong knowledge and skills across all levels. Highly recommended for advanced positions."
    elif avg_score >= 5 and completion >= 60:
        recommendation = "✓ <b>Good performance.</b> The candidate shows solid understanding with room for improvement. Suitable for mid-level positions with mentorship."
    elif avg_score >= 3:
        recommendation = "⚠ <b>Moderate performance.</b> Additional training and practice recommended before considering for professional roles."
    else:
        recommendation = "❌ <b>Needs significant improvement.</b> Consider focused learning program and re-evaluation after 3-6 months of practice."
    
    elements.append(Paragraph(recommendation, styles['Normal']))
    
    # Footer
    elements.append(Spacer(1, 0.5*inch))
    footer = f"<i>Report generated by AI Interview Platform | Contact: support@aiinterview.com</i>"
    elements.append(Paragraph(footer, ParagraphStyle('Footer', parent=styles['Italic'],
                                                     fontSize=9, alignment=TA_CENTER)))
    
    # Build PDF
    doc.build(elements)
    
    # Cleanup temp files
    try:
        for path in chart_paths.values():
            if path and os.path.exists(path):
                os.remove(path)
        os.rmdir(temp_dir)
    except:
        pass
    
    return output_path


# Backward compatibility - use enhanced version by default
generate_user_report_pdf = generate_enhanced_pdf_report


if __name__ == "__main__":
    print("="*70)
    print("Enhanced PDF Report Generator Test")
    print("="*70)
    
    # Test data
    test_data = {
        "user": {
            "username": "John Doe",
            "domain": "Python Programming",
        },
        "sessions": [],
        "level_data": {
            "Level 1 - Basic Fundamentals": [{
                "questions": ["Q1", "Q2", "Q3"],
                "candidate_answers": ["A1", "A2", "A3"],
                "evaluations": [{"score": 7}, {"score": 8}, {"score": 6}],
                "total_score": 7.0,
                "percentage": 70.0,
                "status": "completed",
                "proctoring_warnings": 1,
                "started_at": datetime.now()
            }],
            "Level 2 - Coding Logic": [{
                "questions": ["Q1", "Q2"],
                "candidate_answers": ["A1", "A2"],
                "evaluations": [{"score": 8}, {"score": 9}],
                "total_score": 8.5,
                "percentage": 85.0,
                "status": "completed",
                "proctoring_warnings": 0,
                "started_at": datetime.now()
            }],
            "Level 3 - HR & AI": [{
                "questions": ["Q1", "Q2"],
                "candidate_answers": ["A1", "A2"],
                "evaluations": [{"score": 6}, {"score": 7}],
                "total_score": 6.5,
                "percentage": 65.0,
                "status": "completed",
                "proctoring_warnings": 2,
                "started_at": datetime.now()
            }]
        },
        "statistics": {
            "total_sessions": 3,
            "total_questions": 7,
            "total_answered": 7,
            "average_score": 7.3,
            "total_warnings": 3,
            "completion_rate": 100.0
        }
    }
    
    try:
        pdf_path = generate_enhanced_pdf_report(test_data, "test_enhanced_report.pdf")
        print(f"\n✅ Enhanced PDF generated successfully!")
        print(f"📄 Location: {pdf_path}")
        print(f"\nCharts included:")
        print("  • Performance gauge (speedometer)")
        print("  • Bar chart (level scores)")
        print("  • Pie chart (completion rate)")
        print("  • Radar chart (multi-level analysis)")
    except Exception as e:
        print(f"\n❌ PDF generation failed: {e}")
        import traceback
        traceback.print_exc()
