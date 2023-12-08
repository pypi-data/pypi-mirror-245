const {
  HtmlTag: Re,
  SvelteComponent: st,
  append: M,
  attr: B,
  destroy_each: ot,
  detach: G,
  element: P,
  empty: rt,
  ensure_array_like: he,
  init: at,
  insert: H,
  listen: _t,
  noop: we,
  safe_not_equal: ct,
  set_data: ut,
  space: J,
  text: dt,
  toggle_class: le
} = window.__gradio__svelte__internal;
function ke(n, t, e) {
  const l = n.slice();
  return l[5] = t[e].type, l[6] = t[e].description, l[7] = t[e].default, l[9] = e, l;
}
function ye(n) {
  let t, e = he(
    /*_docs*/
    n[0]
  ), l = [];
  for (let f = 0; f < e.length; f += 1)
    l[f] = qe(ke(n, e, f));
  return {
    c() {
      for (let f = 0; f < l.length; f += 1)
        l[f].c();
      t = rt();
    },
    m(f, s) {
      for (let i = 0; i < l.length; i += 1)
        l[i] && l[i].m(f, s);
      H(f, t, s);
    },
    p(f, s) {
      if (s & /*show_desc, _docs*/
      3) {
        e = he(
          /*_docs*/
          f[0]
        );
        let i;
        for (i = 0; i < e.length; i += 1) {
          const o = ke(f, e, i);
          l[i] ? l[i].p(o, s) : (l[i] = qe(o), l[i].c(), l[i].m(t.parentNode, t));
        }
        for (; i < l.length; i += 1)
          l[i].d(1);
        l.length = e.length;
      }
    },
    d(f) {
      f && G(t), ot(l, f);
    }
  };
}
function ve(n) {
  let t, e, l, f, s, i, o = (
    /*_default*/
    n[7] + ""
  ), a, r, _, u = (
    /*description*/
    n[6] + ""
  ), c;
  return {
    c() {
      t = P("div"), e = P("span"), e.textContent = "default", l = J(), f = P("code"), f.textContent = "=", s = J(), i = new Re(!1), a = J(), r = P("div"), _ = P("p"), c = dt(u), B(e, "class", "svelte-fjhyw9"), B(f, "class", "svelte-fjhyw9"), i.a = null, B(t, "class", "default svelte-fjhyw9"), B(r, "class", "description svelte-fjhyw9");
    },
    m(b, h) {
      H(b, t, h), M(t, e), M(t, l), M(t, f), M(t, s), i.m(o, t), H(b, a, h), H(b, r, h), M(r, _), M(_, c);
    },
    p(b, h) {
      h & /*_docs*/
      1 && o !== (o = /*_default*/
      b[7] + "") && i.p(o), h & /*_docs*/
      1 && u !== (u = /*description*/
      b[6] + "") && ut(c, u);
    },
    d(b) {
      b && (G(t), G(a), G(r));
    }
  };
}
function qe(n) {
  let t, e, l, f = (
    /*type*/
    n[5] + ""
  ), s, i, o, a, r, _;
  function u() {
    return (
      /*click_handler*/
      n[3](
        /*i*/
        n[9]
      )
    );
  }
  let c = (
    /*show_desc*/
    n[1][
      /*i*/
      n[9]
    ] && ve(n)
  );
  return {
    c() {
      t = P("div"), e = P("div"), l = new Re(!1), s = J(), i = P("span"), i.textContent = "▲", o = J(), c && c.c(), a = J(), l.a = s, B(i, "class", "arrow svelte-fjhyw9"), le(i, "hidden", !/*show_desc*/
      n[1][
        /*i*/
        n[9]
      ]), B(e, "class", "type svelte-fjhyw9"), B(t, "class", "param svelte-fjhyw9"), le(
        t,
        "open",
        /*show_desc*/
        n[1][
          /*i*/
          n[9]
        ]
      );
    },
    m(b, h) {
      H(b, t, h), M(t, e), l.m(f, e), M(e, s), M(e, i), M(t, o), c && c.m(t, null), M(t, a), r || (_ = _t(i, "click", u), r = !0);
    },
    p(b, h) {
      n = b, h & /*_docs*/
      1 && f !== (f = /*type*/
      n[5] + "") && l.p(f), h & /*show_desc*/
      2 && le(i, "hidden", !/*show_desc*/
      n[1][
        /*i*/
        n[9]
      ]), /*show_desc*/
      n[1][
        /*i*/
        n[9]
      ] ? c ? c.p(n, h) : (c = ve(n), c.c(), c.m(t, a)) : c && (c.d(1), c = null), h & /*show_desc*/
      2 && le(
        t,
        "open",
        /*show_desc*/
        n[1][
          /*i*/
          n[9]
        ]
      );
    },
    d(b) {
      b && G(t), c && c.d(), r = !1, _();
    }
  };
}
function mt(n) {
  let t, e = (
    /*_docs*/
    n[0] && ye(n)
  );
  return {
    c() {
      t = P("div"), e && e.c(), B(t, "class", "wrap svelte-fjhyw9");
    },
    m(l, f) {
      H(l, t, f), e && e.m(t, null);
    },
    p(l, [f]) {
      /*_docs*/
      l[0] ? e ? e.p(l, f) : (e = ye(l), e.c(), e.m(t, null)) : e && (e.d(1), e = null);
    },
    i: we,
    o: we,
    d(l) {
      l && G(t), e && e.d();
    }
  };
}
function bt(n, t, e) {
  let l, f, { docs: s } = t;
  const i = window.matchMedia("(prefers-color-scheme: dark)");
  i.matches ? console.log("dark mode") : console.log("light mode"), i.addEventListener("change", (a) => {
    console.log(a), a.matches ? e(0, l = Object.entries(s).map(([r, { type: _, description: u, default: c }]) => (console.log({ type: _, description: u, _default: c }), {
      name: r,
      type: _.dark,
      description: u,
      default: c.dark
    }))) : e(0, l = Object.entries(s).map(([r, { type: _, description: u, default: c }]) => (console.log({ type: _, description: u, _default: c }), {
      name: r,
      type: _.light,
      description: u,
      default: c.light
    })));
  });
  const o = (a) => e(1, f[a] = !f[a], f);
  return n.$$set = (a) => {
    "docs" in a && e(2, s = a.docs);
  }, n.$$.update = () => {
    n.$$.dirty & /*docs*/
    4 && e(0, l = Object.entries(s).map(([a, { type: r, description: _, default: u }]) => (console.log({ type: r, description: _, _default: u }), {
      name: a,
      type: r.dark,
      description: _,
      default: u.dark
    }))), n.$$.dirty & /*_docs*/
    1 && console.log(l), n.$$.dirty & /*_docs*/
    1 && e(1, f = l.map((a) => !1));
  }, [l, f, s, o];
}
class pt extends st {
  constructor(t) {
    super(), at(this, t, bt, mt, ct, { docs: 2 });
  }
}
const gt = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], Fe = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
gt.reduce(
  (n, { color: t, primary: e, secondary: l }) => ({
    ...n,
    [t]: {
      primary: Fe[t][e],
      secondary: Fe[t][l]
    }
  }),
  {}
);
function Y(n) {
  let t = ["", "k", "M", "G", "T", "P", "E", "Z"], e = 0;
  for (; n > 1e3 && e < t.length - 1; )
    n /= 1e3, e++;
  let l = t[e];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + l;
}
function ie() {
}
function ht(n, t) {
  return n != n ? t == t : n !== t || n && typeof n == "object" || typeof n == "function";
}
const Ue = typeof window < "u";
let Ce = Ue ? () => window.performance.now() : () => Date.now(), Ke = Ue ? (n) => requestAnimationFrame(n) : ie;
const R = /* @__PURE__ */ new Set();
function Qe(n) {
  R.forEach((t) => {
    t.c(n) || (R.delete(t), t.f());
  }), R.size !== 0 && Ke(Qe);
}
function wt(n) {
  let t;
  return R.size === 0 && Ke(Qe), {
    promise: new Promise((e) => {
      R.add(t = { c: n, f: e });
    }),
    abort() {
      R.delete(t);
    }
  };
}
const X = [];
function kt(n, t = ie) {
  let e;
  const l = /* @__PURE__ */ new Set();
  function f(o) {
    if (ht(n, o) && (n = o, e)) {
      const a = !X.length;
      for (const r of l)
        r[1](), X.push(r, n);
      if (a) {
        for (let r = 0; r < X.length; r += 2)
          X[r][0](X[r + 1]);
        X.length = 0;
      }
    }
  }
  function s(o) {
    f(o(n));
  }
  function i(o, a = ie) {
    const r = [o, a];
    return l.add(r), l.size === 1 && (e = t(f, s) || ie), o(n), () => {
      l.delete(r), l.size === 0 && e && (e(), e = null);
    };
  }
  return { set: f, update: s, subscribe: i };
}
function Le(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function ce(n, t, e, l) {
  if (typeof e == "number" || Le(e)) {
    const f = l - e, s = (e - t) / (n.dt || 1 / 60), i = n.opts.stiffness * f, o = n.opts.damping * s, a = (i - o) * n.inv_mass, r = (s + a) * n.dt;
    return Math.abs(r) < n.opts.precision && Math.abs(f) < n.opts.precision ? l : (n.settled = !1, Le(e) ? new Date(e.getTime() + r) : e + r);
  } else {
    if (Array.isArray(e))
      return e.map(
        (f, s) => ce(n, t[s], e[s], l[s])
      );
    if (typeof e == "object") {
      const f = {};
      for (const s in e)
        f[s] = ce(n, t[s], e[s], l[s]);
      return f;
    } else
      throw new Error(`Cannot spring ${typeof e} values`);
  }
}
function Ve(n, t = {}) {
  const e = kt(n), { stiffness: l = 0.15, damping: f = 0.8, precision: s = 0.01 } = t;
  let i, o, a, r = n, _ = n, u = 1, c = 0, b = !1;
  function h(v, F = {}) {
    _ = v;
    const q = a = {};
    return n == null || F.hard || N.stiffness >= 1 && N.damping >= 1 ? (b = !0, i = Ce(), r = v, e.set(n = _), Promise.resolve()) : (F.soft && (c = 1 / ((F.soft === !0 ? 0.5 : +F.soft) * 60), u = 0), o || (i = Ce(), b = !1, o = wt((d) => {
      if (b)
        return b = !1, o = null, !1;
      u = Math.min(u + c, 1);
      const k = {
        inv_mass: u,
        opts: N,
        settled: !0,
        dt: (d - i) * 60 / 1e3
      }, Z = ce(k, r, n, _);
      return i = d, r = n, e.set(n = Z), k.settled && (o = null), !k.settled;
    })), new Promise((d) => {
      o.promise.then(() => {
        q === a && d();
      });
    }));
  }
  const N = {
    set: h,
    update: (v, F) => h(v(_, n), F),
    subscribe: e.subscribe,
    stiffness: l,
    damping: f,
    precision: s
  };
  return N;
}
const {
  SvelteComponent: yt,
  append: V,
  attr: w,
  component_subscribe: je,
  detach: vt,
  element: qt,
  init: Ft,
  insert: Ct,
  noop: Me,
  safe_not_equal: Lt,
  set_style: ne,
  svg_element: j,
  toggle_class: Ne
} = window.__gradio__svelte__internal, { onMount: Vt } = window.__gradio__svelte__internal;
function jt(n) {
  let t, e, l, f, s, i, o, a, r, _, u, c;
  return {
    c() {
      t = qt("div"), e = j("svg"), l = j("g"), f = j("path"), s = j("path"), i = j("path"), o = j("path"), a = j("g"), r = j("path"), _ = j("path"), u = j("path"), c = j("path"), w(f, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), w(f, "fill", "#FF7C00"), w(f, "fill-opacity", "0.4"), w(f, "class", "svelte-43sxxs"), w(s, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), w(s, "fill", "#FF7C00"), w(s, "class", "svelte-43sxxs"), w(i, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), w(i, "fill", "#FF7C00"), w(i, "fill-opacity", "0.4"), w(i, "class", "svelte-43sxxs"), w(o, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), w(o, "fill", "#FF7C00"), w(o, "class", "svelte-43sxxs"), ne(l, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), w(r, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), w(r, "fill", "#FF7C00"), w(r, "fill-opacity", "0.4"), w(r, "class", "svelte-43sxxs"), w(_, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), w(_, "fill", "#FF7C00"), w(_, "class", "svelte-43sxxs"), w(u, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), w(u, "fill", "#FF7C00"), w(u, "fill-opacity", "0.4"), w(u, "class", "svelte-43sxxs"), w(c, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), w(c, "fill", "#FF7C00"), w(c, "class", "svelte-43sxxs"), ne(a, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), w(e, "viewBox", "-1200 -1200 3000 3000"), w(e, "fill", "none"), w(e, "xmlns", "http://www.w3.org/2000/svg"), w(e, "class", "svelte-43sxxs"), w(t, "class", "svelte-43sxxs"), Ne(
        t,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(b, h) {
      Ct(b, t, h), V(t, e), V(e, l), V(l, f), V(l, s), V(l, i), V(l, o), V(e, a), V(a, r), V(a, _), V(a, u), V(a, c);
    },
    p(b, [h]) {
      h & /*$top*/
      2 && ne(l, "transform", "translate(" + /*$top*/
      b[1][0] + "px, " + /*$top*/
      b[1][1] + "px)"), h & /*$bottom*/
      4 && ne(a, "transform", "translate(" + /*$bottom*/
      b[2][0] + "px, " + /*$bottom*/
      b[2][1] + "px)"), h & /*margin*/
      1 && Ne(
        t,
        "margin",
        /*margin*/
        b[0]
      );
    },
    i: Me,
    o: Me,
    d(b) {
      b && vt(t);
    }
  };
}
function Mt(n, t, e) {
  let l, f, { margin: s = !0 } = t;
  const i = Ve([0, 0]);
  je(n, i, (c) => e(1, l = c));
  const o = Ve([0, 0]);
  je(n, o, (c) => e(2, f = c));
  let a;
  async function r() {
    await Promise.all([i.set([125, 140]), o.set([-125, -140])]), await Promise.all([i.set([-125, 140]), o.set([125, -140])]), await Promise.all([i.set([-125, 0]), o.set([125, -0])]), await Promise.all([i.set([125, 0]), o.set([-125, 0])]);
  }
  async function _() {
    await r(), a || _();
  }
  async function u() {
    await Promise.all([i.set([125, 0]), o.set([-125, 0])]), _();
  }
  return Vt(() => (u(), () => a = !0)), n.$$set = (c) => {
    "margin" in c && e(0, s = c.margin);
  }, [s, l, f, i, o];
}
class Nt extends yt {
  constructor(t) {
    super(), Ft(this, t, Mt, jt, Lt, { margin: 0 });
  }
}
const {
  SvelteComponent: St,
  append: O,
  attr: S,
  binding_callbacks: Se,
  check_outros: We,
  create_component: zt,
  create_slot: Pt,
  destroy_component: Tt,
  destroy_each: xe,
  detach: p,
  element: T,
  empty: Q,
  ensure_array_like: oe,
  get_all_dirty_from_scope: Zt,
  get_slot_changes: At,
  group_outros: $e,
  init: Bt,
  insert: g,
  mount_component: Dt,
  noop: ue,
  safe_not_equal: Et,
  set_data: L,
  set_style: D,
  space: z,
  text: y,
  toggle_class: C,
  transition_in: U,
  transition_out: K,
  update_slot_base: It
} = window.__gradio__svelte__internal, { tick: Ot } = window.__gradio__svelte__internal, { onDestroy: Xt } = window.__gradio__svelte__internal, Yt = (n) => ({}), ze = (n) => ({});
function Pe(n, t, e) {
  const l = n.slice();
  return l[38] = t[e], l[40] = e, l;
}
function Te(n, t, e) {
  const l = n.slice();
  return l[38] = t[e], l;
}
function Gt(n) {
  let t, e = (
    /*i18n*/
    n[1]("common.error") + ""
  ), l, f, s;
  const i = (
    /*#slots*/
    n[29].error
  ), o = Pt(
    i,
    n,
    /*$$scope*/
    n[28],
    ze
  );
  return {
    c() {
      t = T("span"), l = y(e), f = z(), o && o.c(), S(t, "class", "error svelte-1txqlrd");
    },
    m(a, r) {
      g(a, t, r), O(t, l), g(a, f, r), o && o.m(a, r), s = !0;
    },
    p(a, r) {
      (!s || r[0] & /*i18n*/
      2) && e !== (e = /*i18n*/
      a[1]("common.error") + "") && L(l, e), o && o.p && (!s || r[0] & /*$$scope*/
      268435456) && It(
        o,
        i,
        a,
        /*$$scope*/
        a[28],
        s ? At(
          i,
          /*$$scope*/
          a[28],
          r,
          Yt
        ) : Zt(
          /*$$scope*/
          a[28]
        ),
        ze
      );
    },
    i(a) {
      s || (U(o, a), s = !0);
    },
    o(a) {
      K(o, a), s = !1;
    },
    d(a) {
      a && (p(t), p(f)), o && o.d(a);
    }
  };
}
function Ht(n) {
  let t, e, l, f, s, i, o, a, r, _ = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && Ze(n)
  );
  function u(d, k) {
    if (
      /*progress*/
      d[7]
    )
      return Ut;
    if (
      /*queue_position*/
      d[2] !== null && /*queue_size*/
      d[3] !== void 0 && /*queue_position*/
      d[2] >= 0
    )
      return Rt;
    if (
      /*queue_position*/
      d[2] === 0
    )
      return Jt;
  }
  let c = u(n), b = c && c(n), h = (
    /*timer*/
    n[5] && De(n)
  );
  const N = [xt, Wt], v = [];
  function F(d, k) {
    return (
      /*last_progress_level*/
      d[15] != null ? 0 : (
        /*show_progress*/
        d[6] === "full" ? 1 : -1
      )
    );
  }
  ~(s = F(n)) && (i = v[s] = N[s](n));
  let q = !/*timer*/
  n[5] && He(n);
  return {
    c() {
      _ && _.c(), t = z(), e = T("div"), b && b.c(), l = z(), h && h.c(), f = z(), i && i.c(), o = z(), q && q.c(), a = Q(), S(e, "class", "progress-text svelte-1txqlrd"), C(
        e,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), C(
        e,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(d, k) {
      _ && _.m(d, k), g(d, t, k), g(d, e, k), b && b.m(e, null), O(e, l), h && h.m(e, null), g(d, f, k), ~s && v[s].m(d, k), g(d, o, k), q && q.m(d, k), g(d, a, k), r = !0;
    },
    p(d, k) {
      /*variant*/
      d[8] === "default" && /*show_eta_bar*/
      d[18] && /*show_progress*/
      d[6] === "full" ? _ ? _.p(d, k) : (_ = Ze(d), _.c(), _.m(t.parentNode, t)) : _ && (_.d(1), _ = null), c === (c = u(d)) && b ? b.p(d, k) : (b && b.d(1), b = c && c(d), b && (b.c(), b.m(e, l))), /*timer*/
      d[5] ? h ? h.p(d, k) : (h = De(d), h.c(), h.m(e, null)) : h && (h.d(1), h = null), (!r || k[0] & /*variant*/
      256) && C(
        e,
        "meta-text-center",
        /*variant*/
        d[8] === "center"
      ), (!r || k[0] & /*variant*/
      256) && C(
        e,
        "meta-text",
        /*variant*/
        d[8] === "default"
      );
      let Z = s;
      s = F(d), s === Z ? ~s && v[s].p(d, k) : (i && ($e(), K(v[Z], 1, 1, () => {
        v[Z] = null;
      }), We()), ~s ? (i = v[s], i ? i.p(d, k) : (i = v[s] = N[s](d), i.c()), U(i, 1), i.m(o.parentNode, o)) : i = null), /*timer*/
      d[5] ? q && (q.d(1), q = null) : q ? q.p(d, k) : (q = He(d), q.c(), q.m(a.parentNode, a));
    },
    i(d) {
      r || (U(i), r = !0);
    },
    o(d) {
      K(i), r = !1;
    },
    d(d) {
      d && (p(t), p(e), p(f), p(o), p(a)), _ && _.d(d), b && b.d(), h && h.d(), ~s && v[s].d(d), q && q.d(d);
    }
  };
}
function Ze(n) {
  let t, e = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      t = T("div"), S(t, "class", "eta-bar svelte-1txqlrd"), D(t, "transform", e);
    },
    m(l, f) {
      g(l, t, f);
    },
    p(l, f) {
      f[0] & /*eta_level*/
      131072 && e !== (e = `translateX(${/*eta_level*/
      (l[17] || 0) * 100 - 100}%)`) && D(t, "transform", e);
    },
    d(l) {
      l && p(t);
    }
  };
}
function Jt(n) {
  let t;
  return {
    c() {
      t = y("processing |");
    },
    m(e, l) {
      g(e, t, l);
    },
    p: ue,
    d(e) {
      e && p(t);
    }
  };
}
function Rt(n) {
  let t, e = (
    /*queue_position*/
    n[2] + 1 + ""
  ), l, f, s, i;
  return {
    c() {
      t = y("queue: "), l = y(e), f = y("/"), s = y(
        /*queue_size*/
        n[3]
      ), i = y(" |");
    },
    m(o, a) {
      g(o, t, a), g(o, l, a), g(o, f, a), g(o, s, a), g(o, i, a);
    },
    p(o, a) {
      a[0] & /*queue_position*/
      4 && e !== (e = /*queue_position*/
      o[2] + 1 + "") && L(l, e), a[0] & /*queue_size*/
      8 && L(
        s,
        /*queue_size*/
        o[3]
      );
    },
    d(o) {
      o && (p(t), p(l), p(f), p(s), p(i));
    }
  };
}
function Ut(n) {
  let t, e = oe(
    /*progress*/
    n[7]
  ), l = [];
  for (let f = 0; f < e.length; f += 1)
    l[f] = Be(Te(n, e, f));
  return {
    c() {
      for (let f = 0; f < l.length; f += 1)
        l[f].c();
      t = Q();
    },
    m(f, s) {
      for (let i = 0; i < l.length; i += 1)
        l[i] && l[i].m(f, s);
      g(f, t, s);
    },
    p(f, s) {
      if (s[0] & /*progress*/
      128) {
        e = oe(
          /*progress*/
          f[7]
        );
        let i;
        for (i = 0; i < e.length; i += 1) {
          const o = Te(f, e, i);
          l[i] ? l[i].p(o, s) : (l[i] = Be(o), l[i].c(), l[i].m(t.parentNode, t));
        }
        for (; i < l.length; i += 1)
          l[i].d(1);
        l.length = e.length;
      }
    },
    d(f) {
      f && p(t), xe(l, f);
    }
  };
}
function Ae(n) {
  let t, e = (
    /*p*/
    n[38].unit + ""
  ), l, f, s = " ", i;
  function o(_, u) {
    return (
      /*p*/
      _[38].length != null ? Qt : Kt
    );
  }
  let a = o(n), r = a(n);
  return {
    c() {
      r.c(), t = z(), l = y(e), f = y(" | "), i = y(s);
    },
    m(_, u) {
      r.m(_, u), g(_, t, u), g(_, l, u), g(_, f, u), g(_, i, u);
    },
    p(_, u) {
      a === (a = o(_)) && r ? r.p(_, u) : (r.d(1), r = a(_), r && (r.c(), r.m(t.parentNode, t))), u[0] & /*progress*/
      128 && e !== (e = /*p*/
      _[38].unit + "") && L(l, e);
    },
    d(_) {
      _ && (p(t), p(l), p(f), p(i)), r.d(_);
    }
  };
}
function Kt(n) {
  let t = Y(
    /*p*/
    n[38].index || 0
  ) + "", e;
  return {
    c() {
      e = y(t);
    },
    m(l, f) {
      g(l, e, f);
    },
    p(l, f) {
      f[0] & /*progress*/
      128 && t !== (t = Y(
        /*p*/
        l[38].index || 0
      ) + "") && L(e, t);
    },
    d(l) {
      l && p(e);
    }
  };
}
function Qt(n) {
  let t = Y(
    /*p*/
    n[38].index || 0
  ) + "", e, l, f = Y(
    /*p*/
    n[38].length
  ) + "", s;
  return {
    c() {
      e = y(t), l = y("/"), s = y(f);
    },
    m(i, o) {
      g(i, e, o), g(i, l, o), g(i, s, o);
    },
    p(i, o) {
      o[0] & /*progress*/
      128 && t !== (t = Y(
        /*p*/
        i[38].index || 0
      ) + "") && L(e, t), o[0] & /*progress*/
      128 && f !== (f = Y(
        /*p*/
        i[38].length
      ) + "") && L(s, f);
    },
    d(i) {
      i && (p(e), p(l), p(s));
    }
  };
}
function Be(n) {
  let t, e = (
    /*p*/
    n[38].index != null && Ae(n)
  );
  return {
    c() {
      e && e.c(), t = Q();
    },
    m(l, f) {
      e && e.m(l, f), g(l, t, f);
    },
    p(l, f) {
      /*p*/
      l[38].index != null ? e ? e.p(l, f) : (e = Ae(l), e.c(), e.m(t.parentNode, t)) : e && (e.d(1), e = null);
    },
    d(l) {
      l && p(t), e && e.d(l);
    }
  };
}
function De(n) {
  let t, e = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), l, f;
  return {
    c() {
      t = y(
        /*formatted_timer*/
        n[20]
      ), l = y(e), f = y("s");
    },
    m(s, i) {
      g(s, t, i), g(s, l, i), g(s, f, i);
    },
    p(s, i) {
      i[0] & /*formatted_timer*/
      1048576 && L(
        t,
        /*formatted_timer*/
        s[20]
      ), i[0] & /*eta, formatted_eta*/
      524289 && e !== (e = /*eta*/
      s[0] ? `/${/*formatted_eta*/
      s[19]}` : "") && L(l, e);
    },
    d(s) {
      s && (p(t), p(l), p(f));
    }
  };
}
function Wt(n) {
  let t, e;
  return t = new Nt({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      zt(t.$$.fragment);
    },
    m(l, f) {
      Dt(t, l, f), e = !0;
    },
    p(l, f) {
      const s = {};
      f[0] & /*variant*/
      256 && (s.margin = /*variant*/
      l[8] === "default"), t.$set(s);
    },
    i(l) {
      e || (U(t.$$.fragment, l), e = !0);
    },
    o(l) {
      K(t.$$.fragment, l), e = !1;
    },
    d(l) {
      Tt(t, l);
    }
  };
}
function xt(n) {
  let t, e, l, f, s, i = `${/*last_progress_level*/
  n[15] * 100}%`, o = (
    /*progress*/
    n[7] != null && Ee(n)
  );
  return {
    c() {
      t = T("div"), e = T("div"), o && o.c(), l = z(), f = T("div"), s = T("div"), S(e, "class", "progress-level-inner svelte-1txqlrd"), S(s, "class", "progress-bar svelte-1txqlrd"), D(s, "width", i), S(f, "class", "progress-bar-wrap svelte-1txqlrd"), S(t, "class", "progress-level svelte-1txqlrd");
    },
    m(a, r) {
      g(a, t, r), O(t, e), o && o.m(e, null), O(t, l), O(t, f), O(f, s), n[30](s);
    },
    p(a, r) {
      /*progress*/
      a[7] != null ? o ? o.p(a, r) : (o = Ee(a), o.c(), o.m(e, null)) : o && (o.d(1), o = null), r[0] & /*last_progress_level*/
      32768 && i !== (i = `${/*last_progress_level*/
      a[15] * 100}%`) && D(s, "width", i);
    },
    i: ue,
    o: ue,
    d(a) {
      a && p(t), o && o.d(), n[30](null);
    }
  };
}
function Ee(n) {
  let t, e = oe(
    /*progress*/
    n[7]
  ), l = [];
  for (let f = 0; f < e.length; f += 1)
    l[f] = Ge(Pe(n, e, f));
  return {
    c() {
      for (let f = 0; f < l.length; f += 1)
        l[f].c();
      t = Q();
    },
    m(f, s) {
      for (let i = 0; i < l.length; i += 1)
        l[i] && l[i].m(f, s);
      g(f, t, s);
    },
    p(f, s) {
      if (s[0] & /*progress_level, progress*/
      16512) {
        e = oe(
          /*progress*/
          f[7]
        );
        let i;
        for (i = 0; i < e.length; i += 1) {
          const o = Pe(f, e, i);
          l[i] ? l[i].p(o, s) : (l[i] = Ge(o), l[i].c(), l[i].m(t.parentNode, t));
        }
        for (; i < l.length; i += 1)
          l[i].d(1);
        l.length = e.length;
      }
    },
    d(f) {
      f && p(t), xe(l, f);
    }
  };
}
function Ie(n) {
  let t, e, l, f, s = (
    /*i*/
    n[40] !== 0 && $t()
  ), i = (
    /*p*/
    n[38].desc != null && Oe(n)
  ), o = (
    /*p*/
    n[38].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[40]
    ] != null && Xe()
  ), a = (
    /*progress_level*/
    n[14] != null && Ye(n)
  );
  return {
    c() {
      s && s.c(), t = z(), i && i.c(), e = z(), o && o.c(), l = z(), a && a.c(), f = Q();
    },
    m(r, _) {
      s && s.m(r, _), g(r, t, _), i && i.m(r, _), g(r, e, _), o && o.m(r, _), g(r, l, _), a && a.m(r, _), g(r, f, _);
    },
    p(r, _) {
      /*p*/
      r[38].desc != null ? i ? i.p(r, _) : (i = Oe(r), i.c(), i.m(e.parentNode, e)) : i && (i.d(1), i = null), /*p*/
      r[38].desc != null && /*progress_level*/
      r[14] && /*progress_level*/
      r[14][
        /*i*/
        r[40]
      ] != null ? o || (o = Xe(), o.c(), o.m(l.parentNode, l)) : o && (o.d(1), o = null), /*progress_level*/
      r[14] != null ? a ? a.p(r, _) : (a = Ye(r), a.c(), a.m(f.parentNode, f)) : a && (a.d(1), a = null);
    },
    d(r) {
      r && (p(t), p(e), p(l), p(f)), s && s.d(r), i && i.d(r), o && o.d(r), a && a.d(r);
    }
  };
}
function $t(n) {
  let t;
  return {
    c() {
      t = y(" /");
    },
    m(e, l) {
      g(e, t, l);
    },
    d(e) {
      e && p(t);
    }
  };
}
function Oe(n) {
  let t = (
    /*p*/
    n[38].desc + ""
  ), e;
  return {
    c() {
      e = y(t);
    },
    m(l, f) {
      g(l, e, f);
    },
    p(l, f) {
      f[0] & /*progress*/
      128 && t !== (t = /*p*/
      l[38].desc + "") && L(e, t);
    },
    d(l) {
      l && p(e);
    }
  };
}
function Xe(n) {
  let t;
  return {
    c() {
      t = y("-");
    },
    m(e, l) {
      g(e, t, l);
    },
    d(e) {
      e && p(t);
    }
  };
}
function Ye(n) {
  let t = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[40]
  ] || 0)).toFixed(1) + "", e, l;
  return {
    c() {
      e = y(t), l = y("%");
    },
    m(f, s) {
      g(f, e, s), g(f, l, s);
    },
    p(f, s) {
      s[0] & /*progress_level*/
      16384 && t !== (t = (100 * /*progress_level*/
      (f[14][
        /*i*/
        f[40]
      ] || 0)).toFixed(1) + "") && L(e, t);
    },
    d(f) {
      f && (p(e), p(l));
    }
  };
}
function Ge(n) {
  let t, e = (
    /*p*/
    (n[38].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[40]
    ] != null) && Ie(n)
  );
  return {
    c() {
      e && e.c(), t = Q();
    },
    m(l, f) {
      e && e.m(l, f), g(l, t, f);
    },
    p(l, f) {
      /*p*/
      l[38].desc != null || /*progress_level*/
      l[14] && /*progress_level*/
      l[14][
        /*i*/
        l[40]
      ] != null ? e ? e.p(l, f) : (e = Ie(l), e.c(), e.m(t.parentNode, t)) : e && (e.d(1), e = null);
    },
    d(l) {
      l && p(t), e && e.d(l);
    }
  };
}
function He(n) {
  let t, e;
  return {
    c() {
      t = T("p"), e = y(
        /*loading_text*/
        n[9]
      ), S(t, "class", "loading svelte-1txqlrd");
    },
    m(l, f) {
      g(l, t, f), O(t, e);
    },
    p(l, f) {
      f[0] & /*loading_text*/
      512 && L(
        e,
        /*loading_text*/
        l[9]
      );
    },
    d(l) {
      l && p(t);
    }
  };
}
function el(n) {
  let t, e, l, f, s;
  const i = [Ht, Gt], o = [];
  function a(r, _) {
    return (
      /*status*/
      r[4] === "pending" ? 0 : (
        /*status*/
        r[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(e = a(n)) && (l = o[e] = i[e](n)), {
    c() {
      t = T("div"), l && l.c(), S(t, "class", f = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-1txqlrd"), C(t, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), C(
        t,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), C(
        t,
        "generating",
        /*status*/
        n[4] === "generating"
      ), C(
        t,
        "border",
        /*border*/
        n[12]
      ), D(
        t,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), D(
        t,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(r, _) {
      g(r, t, _), ~e && o[e].m(t, null), n[31](t), s = !0;
    },
    p(r, _) {
      let u = e;
      e = a(r), e === u ? ~e && o[e].p(r, _) : (l && ($e(), K(o[u], 1, 1, () => {
        o[u] = null;
      }), We()), ~e ? (l = o[e], l ? l.p(r, _) : (l = o[e] = i[e](r), l.c()), U(l, 1), l.m(t, null)) : l = null), (!s || _[0] & /*variant, show_progress*/
      320 && f !== (f = "wrap " + /*variant*/
      r[8] + " " + /*show_progress*/
      r[6] + " svelte-1txqlrd")) && S(t, "class", f), (!s || _[0] & /*variant, show_progress, status, show_progress*/
      336) && C(t, "hide", !/*status*/
      r[4] || /*status*/
      r[4] === "complete" || /*show_progress*/
      r[6] === "hidden"), (!s || _[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && C(
        t,
        "translucent",
        /*variant*/
        r[8] === "center" && /*status*/
        (r[4] === "pending" || /*status*/
        r[4] === "error") || /*translucent*/
        r[11] || /*show_progress*/
        r[6] === "minimal"
      ), (!s || _[0] & /*variant, show_progress, status*/
      336) && C(
        t,
        "generating",
        /*status*/
        r[4] === "generating"
      ), (!s || _[0] & /*variant, show_progress, border*/
      4416) && C(
        t,
        "border",
        /*border*/
        r[12]
      ), _[0] & /*absolute*/
      1024 && D(
        t,
        "position",
        /*absolute*/
        r[10] ? "absolute" : "static"
      ), _[0] & /*absolute*/
      1024 && D(
        t,
        "padding",
        /*absolute*/
        r[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(r) {
      s || (U(l), s = !0);
    },
    o(r) {
      K(l), s = !1;
    },
    d(r) {
      r && p(t), ~e && o[e].d(), n[31](null);
    }
  };
}
let fe = [], _e = !1;
async function tl(n, t = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
    if (fe.push(n), !_e)
      _e = !0;
    else
      return;
    await Ot(), requestAnimationFrame(() => {
      let e = [0, 0];
      for (let l = 0; l < fe.length; l++) {
        const s = fe[l].getBoundingClientRect();
        (l === 0 || s.top + window.scrollY <= e[0]) && (e[0] = s.top + window.scrollY, e[1] = l);
      }
      window.scrollTo({ top: e[0] - 20, behavior: "smooth" }), _e = !1, fe = [];
    });
  }
}
function ll(n, t, e) {
  let l, { $$slots: f = {}, $$scope: s } = t, { i18n: i } = t, { eta: o = null } = t, { queue: a = !1 } = t, { queue_position: r } = t, { queue_size: _ } = t, { status: u } = t, { scroll_to_output: c = !1 } = t, { timer: b = !0 } = t, { show_progress: h = "full" } = t, { message: N = null } = t, { progress: v = null } = t, { variant: F = "default" } = t, { loading_text: q = "Loading..." } = t, { absolute: d = !0 } = t, { translucent: k = !1 } = t, { border: Z = !1 } = t, { autoscroll: re } = t, W, x = !1, te = 0, E = 0, ae = null, de = 0, I = null, $, A = null, me = !0;
  const nt = () => {
    e(25, te = performance.now()), e(26, E = 0), x = !0, be();
  };
  function be() {
    requestAnimationFrame(() => {
      e(26, E = (performance.now() - te) / 1e3), x && be();
    });
  }
  function pe() {
    e(26, E = 0), x && (x = !1);
  }
  Xt(() => {
    x && pe();
  });
  let ge = null;
  function ft(m) {
    Se[m ? "unshift" : "push"](() => {
      A = m, e(16, A), e(7, v), e(14, I), e(15, $);
    });
  }
  function it(m) {
    Se[m ? "unshift" : "push"](() => {
      W = m, e(13, W);
    });
  }
  return n.$$set = (m) => {
    "i18n" in m && e(1, i = m.i18n), "eta" in m && e(0, o = m.eta), "queue" in m && e(21, a = m.queue), "queue_position" in m && e(2, r = m.queue_position), "queue_size" in m && e(3, _ = m.queue_size), "status" in m && e(4, u = m.status), "scroll_to_output" in m && e(22, c = m.scroll_to_output), "timer" in m && e(5, b = m.timer), "show_progress" in m && e(6, h = m.show_progress), "message" in m && e(23, N = m.message), "progress" in m && e(7, v = m.progress), "variant" in m && e(8, F = m.variant), "loading_text" in m && e(9, q = m.loading_text), "absolute" in m && e(10, d = m.absolute), "translucent" in m && e(11, k = m.translucent), "border" in m && e(12, Z = m.border), "autoscroll" in m && e(24, re = m.autoscroll), "$$scope" in m && e(28, s = m.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, queue, timer_start*/
    169869313 && (o === null ? e(0, o = ae) : a && e(0, o = (performance.now() - te) / 1e3 + o), o != null && (e(19, ge = o.toFixed(1)), e(27, ae = o))), n.$$.dirty[0] & /*eta, timer_diff*/
    67108865 && e(17, de = o === null || o <= 0 || !E ? null : Math.min(E / o, 1)), n.$$.dirty[0] & /*progress*/
    128 && v != null && e(18, me = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (v != null ? e(14, I = v.map((m) => {
      if (m.index != null && m.length != null)
        return m.index / m.length;
      if (m.progress != null)
        return m.progress;
    })) : e(14, I = null), I ? (e(15, $ = I[I.length - 1]), A && ($ === 0 ? e(16, A.style.transition = "0", A) : e(16, A.style.transition = "150ms", A))) : e(15, $ = void 0)), n.$$.dirty[0] & /*status*/
    16 && (u === "pending" ? nt() : pe()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && W && c && (u === "pending" || u === "complete") && tl(W, re), n.$$.dirty[0] & /*status, message*/
    8388624, n.$$.dirty[0] & /*timer_diff*/
    67108864 && e(20, l = E.toFixed(1));
  }, [
    o,
    i,
    r,
    _,
    u,
    b,
    h,
    v,
    F,
    q,
    d,
    k,
    Z,
    W,
    I,
    $,
    A,
    de,
    me,
    ge,
    l,
    a,
    c,
    N,
    re,
    te,
    E,
    ae,
    s,
    f,
    ft,
    it
  ];
}
class nl extends St {
  constructor(t) {
    super(), Bt(
      this,
      t,
      ll,
      el,
      Et,
      {
        i18n: 1,
        eta: 0,
        queue: 21,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: fl,
  assign: il,
  check_outros: sl,
  create_component: et,
  destroy_component: tt,
  detach: ol,
  get_spread_object: rl,
  get_spread_update: al,
  group_outros: _l,
  init: cl,
  insert: ul,
  mount_component: lt,
  safe_not_equal: dl,
  space: ml,
  transition_in: ee,
  transition_out: se
} = window.__gradio__svelte__internal;
function Je(n) {
  let t, e;
  const l = [
    { autoscroll: (
      /*gradio*/
      n[2].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      n[2].i18n
    ) },
    /*loading_status*/
    n[1]
  ];
  let f = {};
  for (let s = 0; s < l.length; s += 1)
    f = il(f, l[s]);
  return t = new nl({ props: f }), {
    c() {
      et(t.$$.fragment);
    },
    m(s, i) {
      lt(t, s, i), e = !0;
    },
    p(s, i) {
      const o = i & /*gradio, loading_status*/
      6 ? al(l, [
        i & /*gradio*/
        4 && { autoscroll: (
          /*gradio*/
          s[2].autoscroll
        ) },
        i & /*gradio*/
        4 && { i18n: (
          /*gradio*/
          s[2].i18n
        ) },
        i & /*loading_status*/
        2 && rl(
          /*loading_status*/
          s[1]
        )
      ]) : {};
      t.$set(o);
    },
    i(s) {
      e || (ee(t.$$.fragment, s), e = !0);
    },
    o(s) {
      se(t.$$.fragment, s), e = !1;
    },
    d(s) {
      tt(t, s);
    }
  };
}
function bl(n) {
  let t, e, l, f = (
    /*loading_status*/
    n[1] && Je(n)
  );
  return e = new pt({ props: { docs: (
    /*value*/
    n[0]
  ) } }), {
    c() {
      f && f.c(), t = ml(), et(e.$$.fragment);
    },
    m(s, i) {
      f && f.m(s, i), ul(s, t, i), lt(e, s, i), l = !0;
    },
    p(s, [i]) {
      /*loading_status*/
      s[1] ? f ? (f.p(s, i), i & /*loading_status*/
      2 && ee(f, 1)) : (f = Je(s), f.c(), ee(f, 1), f.m(t.parentNode, t)) : f && (_l(), se(f, 1, 1, () => {
        f = null;
      }), sl());
      const o = {};
      i & /*value*/
      1 && (o.docs = /*value*/
      s[0]), e.$set(o);
    },
    i(s) {
      l || (ee(f), ee(e.$$.fragment, s), l = !0);
    },
    o(s) {
      se(f), se(e.$$.fragment, s), l = !1;
    },
    d(s) {
      s && ol(t), f && f.d(s), tt(e, s);
    }
  };
}
function pl(n, t, e) {
  let { elem_id: l = "" } = t, { elem_classes: f = [] } = t, { visible: s = !0 } = t, { value: i = !1 } = t, { container: o = !0 } = t, { scale: a = null } = t, { min_width: r = void 0 } = t, { loading_status: _ } = t, { gradio: u } = t;
  return n.$$set = (c) => {
    "elem_id" in c && e(3, l = c.elem_id), "elem_classes" in c && e(4, f = c.elem_classes), "visible" in c && e(5, s = c.visible), "value" in c && e(0, i = c.value), "container" in c && e(6, o = c.container), "scale" in c && e(7, a = c.scale), "min_width" in c && e(8, r = c.min_width), "loading_status" in c && e(1, _ = c.loading_status), "gradio" in c && e(2, u = c.gradio);
  }, [
    i,
    _,
    u,
    l,
    f,
    s,
    o,
    a,
    r
  ];
}
class gl extends fl {
  constructor(t) {
    super(), cl(this, t, pl, bl, dl, {
      elem_id: 3,
      elem_classes: 4,
      visible: 5,
      value: 0,
      container: 6,
      scale: 7,
      min_width: 8,
      loading_status: 1,
      gradio: 2
    });
  }
}
export {
  gl as default
};
