/* ==========================================================================
   Python, SQL & Git — slide deck runtime
   Vanilla JS, no dependencies, works from file:// with no server.

   Markup contract, per deck file:
     <div class="deck">
       <section class="slide" data-title="...">
         <div class="eyebrow">..</div><h2>..</h2>
         <div class="slide-body"> ... </div>
         <aside class="notes"> speaker notes </aside>
       </section>
     </div>

   The footer, progress bar, counter, notes panel and help overlay are all
   injected here so the deck files stay readable.
   ========================================================================== */
(function () {
  "use strict";

  /* ---------------------------------------------------------------- config */
  var meta = document.body.dataset;
  var DECK_LABEL = meta.deck || document.title;
  var STORE_THEME = "pycourse-theme";

  var deck = document.querySelector(".deck");
  if (!deck) return;
  var slides = Array.prototype.slice.call(deck.querySelectorAll(".slide"));
  var current = 0;
  var fragIndex = 0;

  /* ------------------------------------------------- syntax highlighting */
  /* Small hand-rolled tokeniser. Prism-quality is not the goal; "readable on
     a projector, offline, in two themes" is. Highlight <pre><code data-lang>. */

  var PY_KEYWORDS = ("False None True and as assert async await break class continue def del elif " +
    "else except finally for from global if import in is lambda nonlocal not or pass raise " +
    "return try while with yield match case").split(" ");
  var PY_BUILTINS = ("abs all any bool dict enumerate filter float format getattr id input int " +
    "isinstance len list map max min next object open print range repr reversed round set " +
    "sorted str sum tuple type zip Exception ValueError TypeError KeyError IndexError " +
    "NameError ZeroDivisionError FileNotFoundError SyntaxError IndentationError " +
    "AttributeError ImportError self").split(" ");
  var SQL_KEYWORDS = ("select from where group by order having limit offset join inner left right " +
    "full outer on as and or not in between like is null distinct count sum avg min max " +
    "insert into values update set delete create table view index drop alter primary key " +
    "foreign references unique default case when then else end with union all asc desc " +
    "cast integer text real date strftime round coalesce exists").split(" ");
  var SHELL_KEYWORDS = ("cd ls mkdir rm cp mv cat echo python python3 pip git code source " +
    "deactivate export sqlite3 touch pwd which where").split(" ");

  function esc(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function wrap(cls, text) {
    return '<span class="tok-' + cls + '">' + esc(text) + "</span>";
  }

  /* Generic line-oriented tokeniser driven by a small rule table. */
  function highlight(src, lang) {
    if (lang === "text" || lang === "none") return esc(src);
    if (lang === "out" || lang === "output") return highlightOutput(src);

    var kw, bi, comment;
    if (lang === "sql") {
      kw = SQL_KEYWORDS; bi = []; comment = "--";
    } else if (lang === "bash" || lang === "shell") {
      kw = SHELL_KEYWORDS; bi = []; comment = "#";
    } else {
      kw = PY_KEYWORDS; bi = PY_BUILTINS; comment = "#";
    }
    var kwSet = Object.create(null), biSet = Object.create(null);
    kw.forEach(function (w) { kwSet[w.toLowerCase()] = 1; });
    bi.forEach(function (w) { biSet[w] = 1; });

    var out = "";
    var i = 0;
    var n = src.length;

    while (i < n) {
      var ch = src[i];

      // comment to end of line
      if (src.startsWith(comment, i) || (lang !== "sql" && ch === "#")) {
        var eol = src.indexOf("\n", i);
        if (eol === -1) eol = n;
        out += wrap("com", src.slice(i, eol));
        i = eol;
        continue;
      }

      // triple-quoted strings (python docstrings)
      if (lang !== "sql" && (src.startsWith('"""', i) || src.startsWith("'''", i))) {
        var q3 = src.substr(i, 3);
        var close3 = src.indexOf(q3, i + 3);
        var stop3 = close3 === -1 ? n : close3 + 3;
        out += wrap("str", src.slice(i, stop3));
        i = stop3;
        continue;
      }

      // strings, including an f / r / b prefix so f"..." reads as one token
      if (ch === '"' || ch === "'" ||
          (/^[frbu]$/i.test(ch) && (src[i + 1] === '"' || src[i + 1] === "'"))) {
        var open = ch === '"' || ch === "'" ? i : i + 1;
        var quote = src[open];
        var j = open + 1;
        while (j < n && src[j] !== quote) {
          if (src[j] === "\\") j++;
          j++;
        }
        out += wrap("str", src.slice(i, Math.min(j + 1, n)));
        i = j + 1;
        continue;
      }

      // numbers
      if (/[0-9]/.test(ch) && !/[A-Za-z0-9_]/.test(src[i - 1] || " ")) {
        var k = i;
        while (k < n && /[0-9_.eE]/.test(src[k])) k++;
        out += wrap("num", src.slice(i, k));
        i = k;
        continue;
      }

      // words
      if (/[A-Za-z_]/.test(ch)) {
        var w = i;
        while (w < n && /[A-Za-z0-9_]/.test(src[w])) w++;
        var word = src.slice(i, w);
        var lower = word.toLowerCase();
        var isCall = src[w] === "(";
        if (kwSet[lower] && (lang === "sql" || kwSet[word])) {
          out += wrap("kw", word);
        } else if (biSet[word]) {
          out += wrap("bi", word);
        } else if (isCall) {
          out += wrap("fn", word);
        } else {
          out += esc(word);
        }
        i = w;
        continue;
      }

      // operators
      if ("+-*/%=<>!&|^~".indexOf(ch) > -1) {
        out += wrap("op", ch);
        i++;
        continue;
      }

      out += esc(ch);
      i++;
    }
    return out;
  }

  /* Terminal output: colour the prompt, tracebacks and error names. */
  function highlightOutput(src) {
    return src.split("\n").map(function (line) {
      if (/^(\$|>>>|\.\.\.|sqlite>|PS >|C:\\)/.test(line.trim())) {
        var m = line.match(/^(\s*)(\$|>>>|\.\.\.|sqlite>)(.*)$/);
        if (m) return esc(m[1]) + wrap("prompt", m[2]) + esc(m[3]);
      }
      if (/^(Traceback|\s+File ")/.test(line)) return wrap("com", line);
      if (/^[A-Za-z]*(Error|Warning|Exception)\b/.test(line.trim())) return wrap("err", line);
      if (/^(ok|OK|Done|✓|Success)/.test(line.trim())) return wrap("ok", line);
      return esc(line);
    }).join("\n");
  }

  function paintCode() {
    document.querySelectorAll("pre > code").forEach(function (code) {
      if (code.dataset.painted) return;
      var lang = code.dataset.lang || code.closest("figure")?.dataset.lang || "python";
      code.innerHTML = highlight(code.textContent.replace(/^\n/, "").replace(/\s+$/, ""), lang);
      code.dataset.painted = "1";
    });
  }

  /* ------------------------------------------------------- deck furniture */
  function buildChrome() {
    var progress = document.createElement("div");
    progress.id = "progress";
    document.body.appendChild(progress);

    var chrome = document.createElement("div");
    chrome.id = "chrome";
    chrome.innerHTML =
      '<button data-act="prev" title="Previous (←)">‹</button>' +
      '<span id="counter">1 / 1</span>' +
      '<button data-act="next" title="Next (→)">›</button>' +
      '<button data-act="overview" title="Overview (o)">grid</button>' +
      '<button data-act="notes" title="Speaker notes (n)">notes</button>' +
      '<button data-act="theme" title="Light / dark (t)">theme</button>' +
      '<button data-act="help" title="Shortcuts (?)">?</button>';
    document.body.appendChild(chrome);

    var notes = document.createElement("div");
    notes.id = "notes";
    notes.innerHTML = '<h5>Speaker notes</h5><div class="notes-body"></div>';
    document.body.appendChild(notes);

    var help = document.createElement("div");
    help.id = "help";
    help.innerHTML =
      '<div class="panel"><h4>Keyboard shortcuts</h4><table>' +
      "<tr><td><kbd>→</kbd> <kbd>space</kbd></td><td>next step or slide</td></tr>" +
      "<tr><td><kbd>←</kbd></td><td>back</td></tr>" +
      "<tr><td><kbd>↓</kbd> <kbd>↑</kbd></td><td>next / previous slide, skipping steps</td></tr>" +
      "<tr><td><kbd>Home</kbd> <kbd>End</kbd></td><td>first / last slide</td></tr>" +
      "<tr><td><kbd>1</kbd>–<kbd>9</kbd></td><td>jump to slide number</td></tr>" +
      "<tr><td><kbd>o</kbd></td><td>overview grid</td></tr>" +
      "<tr><td><kbd>n</kbd></td><td>speaker notes</td></tr>" +
      "<tr><td><kbd>t</kbd></td><td>light / dark theme</td></tr>" +
      "<tr><td><kbd>f</kbd></td><td>full screen</td></tr>" +
      "<tr><td><kbd>p</kbd></td><td>print / save as PDF</td></tr>" +
      "<tr><td><kbd>esc</kbd></td><td>close this / leave overview</td></tr>" +
      '</table><p class="mt-s" style="font-size:14px;margin-bottom:0">Click the right half of a slide to advance, the left half to go back.</p></div>';
    document.body.appendChild(help);

    chrome.addEventListener("click", function (event) {
      var act = event.target.dataset.act;
      if (!act) return;
      if (act === "prev") back();
      if (act === "next") forward();
      if (act === "overview") toggleOverview();
      if (act === "notes") document.body.classList.toggle("show-notes");
      if (act === "theme") toggleTheme();
      if (act === "help") document.body.classList.toggle("show-help");
    });
  }

  function buildFooters() {
    slides.forEach(function (slide, index) {
      // A slide is a three-row grid: head / body / footer. Decks are authored
      // as a flat list of elements, so group them into those rows here —
      // otherwise the h2 lands in the 1fr row and shoves the content down.
      if (!slide.matches(".slide--title, .slide--section") && !slide.querySelector(".slide-head")) {
        var head = document.createElement("div");
        head.className = "slide-head";
        var body = document.createElement("div");
        body.className = "slide-body";
        var existingBody = slide.querySelector(".slide-body");

        Array.prototype.slice.call(slide.children).forEach(function (el) {
          if (el.matches("aside.notes, .slide-footer")) return;
          if (el === existingBody) return;
          if (el.matches(".eyebrow, h2, .subtitle")) head.appendChild(el);
          else body.appendChild(el);
        });

        slide.insertBefore(head, slide.firstChild);
        if (existingBody) {
          Array.prototype.slice.call(body.children).forEach(function (el) {
            existingBody.appendChild(el);
          });
        } else {
          head.parentNode.insertBefore(body, head.nextSibling);
        }
      }

      if (!slide.querySelector(".slide-footer")) {
        var footer = document.createElement("div");
        footer.className = "slide-footer";
        footer.innerHTML =
          "<span>" + DECK_LABEL + "</span>" +
          '<span class="where">' + (index + 1) + " / " + slides.length + "</span>";
        slide.appendChild(footer);
      }
    });
  }

  /* ---------------------------------------------------------- navigation */
  function frags(slide) {
    return Array.prototype.slice.call(slide.querySelectorAll(".frag"));
  }

  function render() {
    slides.forEach(function (slide, index) {
      slide.classList.toggle("is-active", index === current);
    });
    var slide = slides[current];
    frags(slide).forEach(function (el, index) {
      el.classList.toggle("is-shown", index < fragIndex);
    });

    document.getElementById("counter").textContent = (current + 1) + " / " + slides.length;
    document.getElementById("progress").style.width =
      ((current + 1) / slides.length * 100) + "%";

    var note = slide.querySelector("aside.notes");
    document.querySelector("#notes .notes-body").innerHTML =
      note ? note.innerHTML : '<p style="color:var(--ink-dim)">No notes for this slide.</p>';

    if (history.replaceState) history.replaceState(null, "", "#" + (current + 1));
    document.title = (slide.dataset.title ? slide.dataset.title + " — " : "") + DECK_LABEL;
  }

  function go(index, showAllFrags) {
    current = Math.max(0, Math.min(slides.length - 1, index));
    fragIndex = showAllFrags ? frags(slides[current]).length : 0;
    render();
  }

  function forward() {
    var total = frags(slides[current]).length;
    if (fragIndex < total) { fragIndex++; render(); return; }
    if (current < slides.length - 1) go(current + 1, false);
  }

  function back() {
    if (fragIndex > 0) { fragIndex--; render(); return; }
    if (current > 0) go(current - 1, true);
  }

  function toggleTheme() {
    var next = document.documentElement.dataset.theme === "light" ? "dark" : "light";
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem(STORE_THEME, next); } catch (e) { /* private mode */ }
  }

  /* ------------------------------------------------------- overview mode */
  var overviewCells = null;

  function toggleOverview() {
    var on = !document.body.classList.contains("is-overview");
    document.body.classList.toggle("is-overview", on);

    if (on) {
      // Each slide goes in a clipping cell so the 0.228 scale tiles neatly.
      overviewCells = slides.map(function (slide, index) {
        var cell = document.createElement("div");
        cell.className = "ov-cell" + (index === current ? " is-current" : "");
        cell.innerHTML = '<span class="ov-num">' + (index + 1) + "</span>";
        slide.parentNode.insertBefore(cell, slide);
        cell.appendChild(slide);
        cell.addEventListener("click", function () {
          toggleOverview();
          go(index, true);
        });
        return cell;
      });
      slides.forEach(function (s) { s.classList.add("is-active"); });
      if (overviewCells[current]) {
        overviewCells[current].scrollIntoView({ block: "center" });
      }
    } else if (overviewCells) {
      overviewCells.forEach(function (cell) {
        var slide = cell.querySelector(".slide");
        cell.parentNode.insertBefore(slide, cell);
        cell.remove();
      });
      overviewCells = null;
      render();
      fit();
    }
  }

  /* ------------------------------------------------- scale stage to window */
  function fit() {
    if (document.body.classList.contains("is-overview")) return;
    var pad = 36;
    var scale = Math.min(
      (window.innerWidth - pad) / 1280,
      (window.innerHeight - pad) / 720
    );
    deck.style.transform = "scale(" + scale.toFixed(4) + ")";
  }

  /* ------------------------------------------------------------ bindings */
  function onKey(event) {
    if (event.metaKey || event.ctrlKey || event.altKey) return;
    var key = event.key;

    if (key === "Escape") {
      if (document.body.classList.contains("show-help")) {
        document.body.classList.remove("show-help");
      } else if (document.body.classList.contains("is-overview")) {
        toggleOverview();
      }
      return;
    }

    switch (key) {
      case "ArrowRight": case " ": case "PageDown": case "Enter":
        event.preventDefault(); forward(); break;
      case "ArrowLeft": case "PageUp": case "Backspace":
        event.preventDefault(); back(); break;
      case "ArrowDown":
        event.preventDefault(); go(current + 1, false); break;
      case "ArrowUp":
        event.preventDefault(); go(current - 1, false); break;
      case "Home": go(0, false); break;
      case "End": go(slides.length - 1, true); break;
      case "o": case "O": toggleOverview(); break;
      case "n": case "N": document.body.classList.toggle("show-notes"); break;
      case "t": case "T": toggleTheme(); break;
      case "?": case "h": document.body.classList.toggle("show-help"); break;
      case "p": case "P": window.print(); break;
      case "f": case "F":
        if (document.fullscreenElement) document.exitFullscreen();
        else document.documentElement.requestFullscreen?.();
        break;
      default:
        if (/^[1-9]$/.test(key)) go(parseInt(key, 10) - 1, false);
    }
  }

  function bindPointer() {
    document.getElementById("viewport").addEventListener("click", function (event) {
      if (document.body.classList.contains("is-overview")) return;
      if (event.target.closest("a, button, pre, table")) return;
      if (event.clientX < window.innerWidth * 0.35) back();
      else forward();
    });

    var touchX = null;
    document.addEventListener("touchstart", function (e) { touchX = e.touches[0].clientX; }, { passive: true });
    document.addEventListener("touchend", function (e) {
      if (touchX === null) return;
      var dx = e.changedTouches[0].clientX - touchX;
      if (Math.abs(dx) > 55) { dx < 0 ? forward() : back(); }
      touchX = null;
    }, { passive: true });
  }

  /* ----------------------------------------------------------------- boot */
  try {
    var saved = localStorage.getItem(STORE_THEME);
    if (saved) document.documentElement.dataset.theme = saved;
  } catch (e) { /* ignore */ }

  paintCode();
  buildChrome();
  buildFooters();

  var fromHash = parseInt((location.hash || "").replace("#", ""), 10);
  go(isNaN(fromHash) ? 0 : fromHash - 1, false);

  fit();
  window.addEventListener("resize", fit);
  document.addEventListener("keydown", onKey);
  bindPointer();
})();
