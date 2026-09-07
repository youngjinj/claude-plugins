#!/usr/bin/env python3
"""md2html - Markdown -> self-contained HTML with a 260px sticky TOC, 1280px layout.

Implements the layout/typography spec in SKILL.md. Supports the markdown subset
used by engineering notes: headings, tables, fenced code, lists, task lists,
blockquotes, hr, inline code/bold/italic/links.

Usage:  md2html.py FILE.md [FILE.md ...]
Output: FILE.html next to each input.
"""

import html
import os
import re
import sys

CSS = """
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:#eceef4;color:#22232b;
 font-family:system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans KR","Malgun Gothic",sans-serif;
 font-size:15px;line-height:1.7}
.wrap{max-width:1280px;margin:0 auto;display:flex;align-items:flex-start;gap:0;
 background:#fff;box-shadow:0 0 24px rgba(0,0,0,.08);min-height:100vh}
nav.toc{flex:0 0 260px;width:260px;align-self:flex-start;position:sticky;top:0;height:100vh;
 overflow-y:auto;background:#1a1a2e;color:#c9cbd6;padding:24px 0 40px}
nav.toc .toc-title{font-size:11px;letter-spacing:.14em;text-transform:uppercase;
 color:#6c7086;padding:0 20px 12px}
nav.toc a{display:block;color:#c9cbd6;text-decoration:none;padding:4px 20px;
 border-left:3px solid transparent;word-break:keep-all}
nav.toc a:hover{background:#23233f;color:#fff}
nav.toc a.active{color:#8be9fd;border-left-color:#8be9fd;background:#22223c}
nav.toc a.toc-h2{font-weight:600;margin-top:8px;font-size:13px}
nav.toc a.toc-h3{padding-left:36px;font-size:12px}
nav.toc a.toc-h4{padding-left:48px;font-size:11.5px}
main{flex:1 1 auto;min-width:0;padding:40px 48px 120px}
h1{font-size:28px;line-height:1.35;margin:0 0 24px;padding-bottom:12px;
 border-bottom:3px solid #4361ee;word-break:keep-all}
h2{font-size:22px;margin:48px 0 16px;padding-bottom:8px;border-bottom:2px solid #e8e8f0;
 scroll-margin-top:16px;word-break:keep-all}
h3{font-size:17px;margin:32px 0 12px;scroll-margin-top:16px;word-break:keep-all}
h4{font-size:15px;margin:24px 0 10px;scroll-margin-top:16px;word-break:keep-all}
p{margin:0 0 14px}
a{color:#3049c9}
hr{border:0;border-top:1px solid #e2e3ec;margin:32px 0}
ul,ol{margin:0 0 14px;padding-left:24px}
li{margin:3px 0}
code{background:#f0f1f6;color:#c7254e;font-size:13px;padding:1px 5px;border-radius:4px;
 font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
pre{background:#1e1e2e;color:#cdd6f4;border-radius:8px;padding:16px 18px;overflow-x:auto;
 margin:0 0 18px;font-size:12.5px;line-height:1.55}
pre code{background:none;color:inherit;padding:0;font-size:inherit}
pre .cm{color:#6c7086}
pre .kw{color:#cba6f7}
pre .st{color:#a6e3a1}
table{width:100%;border-collapse:collapse;margin:0 0 20px;font-size:14px}
th,td{text-align:left;padding:7px 10px;border-bottom:1px solid #e8e8f0;vertical-align:top}
th{background:#f0f1f6;border-bottom:2px solid #d7d9e4;font-weight:600;white-space:nowrap}
tbody tr:hover{background:#f8f8fc}
td code,th code{white-space:nowrap}
blockquote{margin:0 0 18px;padding:2px 16px;border-left:4px solid #cbd0e0;color:#4a4c5a;
 background:#f7f8fc}
blockquote p:last-child{margin-bottom:0}
.callout{margin:0 0 18px;padding:12px 16px;border-radius:8px;border:1px solid}
.callout-warning{background:#fff8e1;border-color:#f0d48a}
.callout-info{background:#eef4ff;border-color:#b9cdf5}
.callout-note{background:#f5f0ff;border-color:#d3c4f2}
.chk{display:inline-block;width:13px;height:13px;border:1.5px solid #9aa0b4;border-radius:3px;
 margin-right:7px;vertical-align:-1px}
li.task{list-style:none;margin-left:-20px}
#top{position:fixed;right:24px;bottom:24px;display:none;background:#1a1a2e;color:#fff;
 border:0;border-radius:22px;padding:10px 16px;font-size:13px;cursor:pointer;
 box-shadow:0 2px 10px rgba(0,0,0,.25)}
@media (max-width:900px){nav.toc{display:none}main{padding:24px 20px 80px}}
"""

JS = """
(function(){
 var links=[].slice.call(document.querySelectorAll('nav.toc a'));
 var heads=links.map(function(a){return document.getElementById(a.getAttribute('href').slice(1))});
 var nav=document.querySelector('nav.toc');
 function spy(){
  var i,cur=0;
  for(i=0;i<heads.length;i++){if(heads[i]&&heads[i].getBoundingClientRect().top<=90)cur=i}
  links.forEach(function(a,j){a.classList.toggle('active',j===cur)});
  var a=links[cur];
  if(a&&nav){var r=a.getBoundingClientRect(),n=nav.getBoundingClientRect();
   if(r.top<n.top||r.bottom>n.bottom)nav.scrollTop+=r.top-n.top-n.height/2}
  document.getElementById('top').style.display=window.scrollY>400?'block':'none';
 }
 links.forEach(function(a){a.addEventListener('click',function(e){
  e.preventDefault();var t=document.getElementById(a.getAttribute('href').slice(1));
  if(t){t.scrollIntoView({behavior:'smooth'});history.replaceState(null,'',a.getAttribute('href'))}
 })});
 document.getElementById('top').addEventListener('click',function(){
  window.scrollTo({top:0,behavior:'smooth'})});
 window.addEventListener('scroll',spy,{passive:true});spy();
})();
"""

C_KEYWORDS = r"""\b(?:if|else|while|for|do|return|break|continue|switch|case|default|goto|
struct|typedef|static|extern|const|void|int|char|short|long|unsigned|signed|bool|sizeof|
NULL|true|false|assert)\b"""


def highlight(code: str, lang: str) -> str:
    """Escape and add .cm/.kw/.st spans. Order matters: comments, strings, keywords."""
    out = []
    for line in code.split("\n"):
        esc = html.escape(line)
        # whole-line comment forms first
        m = re.match(r"^\s*(#|//|/\*|\*\s)", line)
        if m and not line.lstrip().startswith("#include"):
            out.append('<span class="cm">%s</span>' % esc)
            continue
        # trailing comment
        esc = re.sub(r"(\s)(#[^&]*|//.*|/\*.*?\*/)$", r'\1<span class="cm">\2</span>', esc)
        # keywords and strings only for explicitly tagged fences -- an untagged fence is
        # usually pseudocode or an ASCII diagram, where highlighting reads as noise
        if lang in ("c", "cpp", "h", "hpp"):
            esc = re.sub(r"(&quot;[^&]*?&quot;)", r'<span class="st">\1</span>', esc)
            esc = re.sub(C_KEYWORDS, r'<span class="kw">\g<0></span>', esc, flags=re.X)
        out.append(esc)
    return "\n".join(out)


def inline(text: str) -> str:
    """Inline markdown -> HTML. Code spans are protected from further substitution."""
    spans = []

    def stash(m):
        spans.append("<code>%s</code>" % html.escape(m.group(1)))
        return "\x00%d\x00" % (len(spans) - 1)

    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text)
    # local .md links point at the generated sibling .html
    text = re.sub(r"\[([^\]]+)\]\((?!\w+:)([^)#]+)\.md(#[^)]*)?\)",
                  r'<a href="\2.html\3">\1</a>', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], text)


def slug(counters, level):
    if level == 2:
        counters[2] += 1
        counters[3] = counters[4] = 0
        return "sec%d" % counters[2]
    if level == 3:
        counters[3] += 1
        counters[4] = 0
        return "sec%d-%d" % (counters[2], counters[3])
    counters[4] += 1
    return "sec%d-%d-%d" % (counters[2], counters[3], counters[4])


def render_row(cells, tag):
    return "<tr>%s</tr>" % "".join("<%s>%s</%s>" % (tag, inline(c), tag) for c in cells)


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", line)]


def convert(md: str):
    lines = md.split("\n")
    body, toc = [], []
    counters = {2: 0, 3: 0, 4: 0}
    i, n = 0, len(lines)
    title = None

    def close_list(stack):
        while stack:
            body.append("</%s>" % stack.pop())

    list_stack = []

    while i < n:
        line = lines[i]

        # fenced code
        m = re.match(r"^```(\w*)\s*$", line)
        if m:
            close_list(list_stack)
            lang, buf, i = m.group(1), [], i + 1
            while i < n and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            body.append("<pre><code>%s</code></pre>" % highlight("\n".join(buf), lang))
            continue

        # heading
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            close_list(list_stack)
            level, text = len(m.group(1)), m.group(2).strip()
            if level == 1:
                title = re.sub(r"<[^>]+>", "", inline(text))
                body.append("<h1>%s</h1>" % inline(text))
            else:
                sid = slug(counters, level)
                body.append('<h%d id="%s">%s</h%d>' % (level, sid, inline(text), level))
                toc.append('<a class="toc-h%d" href="#%s">%s</a>'
                           % (level, sid, re.sub(r"<[^>]+>", "", inline(text))))
            i += 1
            continue

        # table
        if line.lstrip().startswith("|") and i + 1 < n and re.match(
                r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            close_list(list_stack)
            head = split_row(line)
            i += 2
            rows = []
            while i < n and lines[i].lstrip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            body.append("<table><thead>%s</thead><tbody>%s</tbody></table>"
                        % (render_row(head, "th"),
                           "".join(render_row(r, "td") for r in rows)))
            continue

        # hr
        if re.match(r"^\s*---+\s*$", line):
            close_list(list_stack)
            body.append("<hr>")
            i += 1
            continue

        # blockquote
        if line.lstrip().startswith(">"):
            close_list(list_stack)
            buf = []
            while i < n and lines[i].lstrip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            body.append("<blockquote>%s</blockquote>"
                        % "".join("<p>%s</p>" % inline(p) for p in
                                  re.split(r"\n\s*\n", "\n".join(buf)) if p.strip()))
            continue

        # list item
        m = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.*)$", line)
        if m:
            indent, marker, text = len(m.group(1)), m.group(2), m.group(3)
            tag = "ul" if marker in "-*+" else "ol"
            depth = indent // 2
            while len(list_stack) > depth + 1:
                body.append("</%s>" % list_stack.pop())
            if len(list_stack) < depth + 1:
                body.append("<%s>" % tag)
                list_stack.append(tag)
            task = re.match(r"^\[([ xX])\]\s+(.*)$", text)
            if task:
                body.append('<li class="task"><span class="chk"></span>%s</li>'
                            % inline(task.group(2)))
            else:
                body.append("<li>%s</li>" % inline(text))
            i += 1
            continue

        # blank
        if not line.strip():
            close_list(list_stack)
            i += 1
            continue

        # paragraph
        close_list(list_stack)
        buf = []
        while i < n and lines[i].strip() and not re.match(
                r"^(#{1,4}\s|```|\s*\||\s*---+\s*$|\s*>|\s*([-*+]|\d+\.)\s)", lines[i]):
            buf.append(lines[i].strip())
            i += 1
        para = " ".join(buf)
        cls = None
        if re.match(r"^\*\*(주의|경고|Warning)", para):
            cls = "callout callout-warning"
        elif re.match(r"^\*\*(참고|Note)", para):
            cls = "callout callout-note"
        body.append('<div class="%s">%s</div>' % (cls, inline(para)) if cls
                    else "<p>%s</p>" % inline(para))

    close_list(list_stack)
    return title or "document", "\n".join(toc), "\n".join(body)


def main(paths):
    for path in paths:
        with open(path, encoding="utf-8") as f:
            title, toc, body = convert(f.read())
        out = os.path.splitext(path)[0] + ".html"
        with open(out, "w", encoding="utf-8") as f:
            f.write(
                '<!DOCTYPE html>\n<html lang="ko"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1">'
                "<title>%s</title><style>%s</style></head><body>"
                '<div class="wrap"><nav class="toc"><div class="toc-title">Contents</div>%s</nav>'
                '<main>%s</main></div><button id="top">맨 위로</button>'
                "<script>%s</script></body></html>\n"
                % (html.escape(title), CSS, toc, body, JS))
        print(out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: md2html.py FILE.md [FILE.md ...]")
    main(sys.argv[1:])
