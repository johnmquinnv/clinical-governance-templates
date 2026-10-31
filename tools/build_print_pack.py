# SPDX-License-Identifier: MIT
"""Build matching PDF and HTML editions directly from the source Markdown."""
from pathlib import Path
from html import escape
import re
from urllib.parse import urljoin
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4

ROOT=Path(__file__).resolve().parents[1]
BLUE=colors.HexColor('#163842')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle('BodyQ',fontName='Helvetica',fontSize=9.5,leading=12.5,spaceAfter=5,textColor=BLUE))
styles.add(ParagraphStyle('TitleQ',fontName='Helvetica-Bold',fontSize=21,leading=25,spaceAfter=10,textColor=BLUE))
styles.add(ParagraphStyle('H2Q',fontName='Helvetica-Bold',fontSize=12,leading=16,spaceBefore=13,spaceAfter=6,textColor=BLUE,keepWithNext=True))
styles.add(ParagraphStyle('H3Q',fontName='Helvetica-Bold',fontSize=10,leading=14,spaceBefore=8,spaceAfter=5,textColor=BLUE,keepWithNext=True))
styles.add(ParagraphStyle('CellQ',fontName='Helvetica',fontSize=8,leading=11,textColor=BLUE))
styles.add(ParagraphStyle('NoteQ',fontName='Helvetica',fontSize=8,leading=11,spaceAfter=8,textColor=colors.HexColor('#4d6e78')))

def plain(text):
    for char in ['\u2010','\u2011','\u2012','\u2013','\u2014','\u2212']:
        text=text.replace(char,'-')
    return text.replace('\u2018',"'").replace('\u2019',"'").replace('\u201c','"').replace('\u201d','"').replace('→','->').replace('\u00a0',' ')

def inline(text,base,html=False):
    text=escape(plain(text))
    def link(m):
        target=urljoin(base,m[2])
        return ('<a href="'+escape(target,quote=True)+'">'+m[1]+'</a>')
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,text)
    text=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',text)
    text=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',text)
    return text

def parse(text,base,width):
    story=[];out=[];lines=text.splitlines();i=0
    while i<len(lines):
        line=lines[i].strip();i+=1
        if not line: continue
        if line.startswith('|'):
            rows=[]
            while True:
                parts=[x.strip() for x in line.strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',x or ' ') for x in parts): rows.append(parts)
                if i>=len(lines) or not lines[i].strip().startswith('|'): break
                line=lines[i].strip();i+=1
            n=max(map(len,rows));rows=[r+['']*(n-len(r)) for r in rows]
            table=Table([[Paragraph(inline(v,base),styles['CellQ']) for v in r] for r in rows],colWidths=[width/n]*n,repeatRows=1,hAlign='LEFT')
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5eff1')),('GRID',(0,0),(-1,-1),.45,colors.HexColor('#bfd0d5')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
            story.extend([table,Spacer(1,8)])
            out.append('<table>'+''.join('<tr>'+''.join('<'+('th' if j==0 else 'td')+'>'+inline(v,base,True)+'</'+('th' if j==0 else 'td')+'>' for v in row)+'</tr>' for j,row in enumerate(rows))+'</table>')
            continue
        h=re.match(r'^(#{1,3})\s+(.+)',line)
        if h:
            level=len(h[1]);style={1:'TitleQ',2:'H2Q',3:'H3Q'}[level]
            story.append(Paragraph(inline(h[2],base),styles[style]));out.append(f'<h{level}>'+inline(h[2],base,True)+f'</h{level}>');continue
        if line=='---': continue
        line=re.sub(r'^>\s*','',line)
        is_list = line.startswith('- ')
        if is_list: line=line[2:]
        paragraph = Paragraph(inline(line,base),styles['BodyQ'])
        next_content = next((s.strip() for s in lines[i:] if s.strip()), '')
        if next_content.startswith('- '):
            paragraph.keepWithNext = True
        story.append(paragraph)
        out.append('<p>'+inline(line,base,True)+'</p>')
    return story,'\n'.join(out)

def build(repo,slug,title,paths):
    target=ROOT/'downloads';target.mkdir(exist_ok=True)
    story=[];sections=[]
    notice='John Quinn, MD, MPH, PhD, EMT-P | Printable edition: October 31, 2026 | Educational draft; independent clinical sign-off is not recorded. Adapt and obtain local approval before operational use. Original content: CC BY-NC 4.0. Source guidance dates remain as recorded in each checklist or template.'
    for index,path in enumerate(paths):
        if index: story.append(PageBreak())
        base=f'https://github.com/johnmquinnv/{repo}/blob/main/{path}'
        story.append(Paragraph(title.upper(),styles['NoteQ']))
        story.append(Paragraph(notice,styles['NoteQ']))
        content=(ROOT/path).read_text()
        blocks,html=parse(content,base,A4[0]-88)
        story.extend(blocks)
        story.append(Spacer(1,8))
        story.append(Paragraph('Editable source: <a href="'+base+'">'+escape(path)+'</a>',styles['NoteQ']))
        sections.append('<section><div class="edition">'+escape(title)+' · October 31, 2026</div><p class="notice">'+escape(notice)+'</p>'+html+'<p class="source">Editable source: <a href="'+base+'">'+escape(path)+'</a></p></section>')
    def footer(canvas,doc):
        canvas.saveState();canvas.setStrokeColor(colors.HexColor('#bfd0d5'));canvas.line(44,40,A4[0]-44,40);canvas.setFont('Helvetica',8);canvas.setFillColor(BLUE);canvas.drawString(44,27,'John Quinn | Educational resources | CC BY-NC 4.0');canvas.drawRightString(A4[0]-44,27,str(doc.page));canvas.restoreState()
    pdf=target/(slug+'.pdf')
    SimpleDocTemplate(str(pdf),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=40,bottomMargin=55,title=title,author='John Quinn').build(story,onFirstPage=footer,onLaterPages=footer)
    html='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(title)+'</title><style>body{font:15px/1.6 Helvetica,Arial,sans-serif;color:#163842;margin:40px auto;max-width:900px;padding:0 24px}h1{font-size:30px;line-height:1.2}h2{font-size:21px;margin-top:28px}h3{font-size:17px}a{color:#086274}section{margin-bottom:60px}.edition{font-weight:bold;text-transform:uppercase;font-size:12px;letter-spacing:.08em}.notice,.source{font-size:12px;color:#4d6e78}table{border-collapse:collapse;width:100%;table-layout:fixed;font-size:13px}th,td{border:1px solid #bfd0d5;padding:10px;text-align:left;vertical-align:top;overflow-wrap:anywhere}th{background:#e5eff1}button{padding:10px 20px;font:inherit;background:#163842;color:white;border:0;border-radius:6px}@media print{@page{size:A4;margin:16mm}body{font-size:10pt;line-height:1.4;max-width:none;margin:0;padding:0}.toolbar{display:none}section{break-before:page}section:first-of-type{break-before:auto}h1,h2,h3{break-after:avoid}tr{break-inside:avoid}.notice,.source{font-size:8pt}table{font-size:8pt}th,td{padding:7px}}</style></head><body><div class="toolbar"><button onclick="window.print()" type="button">Print this pack</button> <a href="'+slug+'.pdf">Download PDF</a></div>'+''.join(sections)+'</body></html>'
    (target/(slug+'.html')).write_text(html)
    print(pdf)

build('clinical-governance-templates','clinical-governance-templates','Clinical governance templates',['templates/clinical-audit.md','templates/incident-review.md','templates/qi-project-plan.md'])
