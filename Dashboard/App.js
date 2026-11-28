"use strict";

const byId = id => document.getElementById(id);
const number = new Intl.NumberFormat("zh-CN");
const dates = new Intl.DateTimeFormat("zh-CN", {
  timeZone: "Asia/Shanghai", month: "2-digit", day: "2-digit",
  hour: "2-digit", minute: "2-digit", hourCycle: "h23"
});
const showDate = time => dates.format(new Date(time));
const fullDate = time => new Intl.DateTimeFormat("zh-CN", {
  timeZone: "Asia/Shanghai", year: "numeric", month: "2-digit", day: "2-digit",
  hour: "2-digit", minute: "2-digit", hourCycle: "h23"
}).format(new Date(time));
const fmt = value => number.format(value);
const sign = value => value > 0 ? "+" + fmt(value) : fmt(value);
const pageSize = 15;
let data;
let page = 0;
let trendPoints = [];

function el(tag, text = "", className = "") {
  const node = document.createElement(tag);
  node.textContent = text;
  if (className) node.className = className;
  return node;
}

function link(text, href) {
  const node = el("a", text);
  node.href = href;
  return node;
}

function renderBars(id, rows, maximum) {
  byId(id).replaceChildren(...rows.map(row => {
    const node = el("div", "", "bar-row");
    const track = el("div", "", "bar-track");
    track.setAttribute("aria-hidden", "true");
    for (const [amount, style] of row.segments) {
      const bar = el("div", "", "bar-fill " + style);
      bar.style.width = Math.abs(amount) / Math.max(1, maximum) * 100 + "%";
      track.append(bar);
    }
    node.append(el("span", row.label), track, el("span", row.value, "bar-value"));
    return node;
  }));
}

function renderMetrics() {
  const percent = (data.closed / data.total * 100).toFixed(2) + "%";
  const entries = [
    ["已闭合分片", fmt(data.closed), `共 ${fmt(data.total)} 片 · ${percent}`],
    ["开放分片", fmt(data.open), `其中 ${fmt(data.singletons)} 片只余一个指数`],
    ["待证精确键", fmt(data.keys), "去重后的 (p, e) 对"],
    ["已全闭的规范根", fmt(data.roots.filter(row => !row.open).length), `共 ${data.roots.length} 个规范根`]
  ];
  byId("metrics").replaceChildren(...entries.map(([label, value, meta]) => {
    const node = el("article", "", "metric");
    node.append(el("div", label, "name"), el("div", value, "value"), el("div", meta, "meta"));
    return node;
  }));
}

function renderBreakdowns() {
  const recent = data.history.slice(1).map((entry, index) => ({
    label: showDate(entry.timestamp), delta: entry.closed - data.history[index].closed
  })).filter(entry => entry.delta !== 0).slice(-6).reverse();
  renderBars("batches", recent.map(({label, delta}) => ({
    label, segments: [[delta, delta < 0 ? "reopened" : ""]], value: sign(delta)
  })), Math.max(...recent.map(entry => Math.abs(entry.delta))));

  renderBars("roots", data.roots.map(row => ({
    label: "p = " + row.root, segments: [[(row.total - row.open) / row.total, ""]],
    value: `${row.total - row.open} / ${row.total}`
  })), 1);
  renderBars("keys", data.roots.map(row => ({
    label: "p = " + row.root, segments: [[row.keys, ""]], value: row.keys
  })), Math.max(...data.roots.map(row => row.keys)));

  const totals = new Map();
  for (const {model, closed, overlap} of data.credits) {
    const total = totals.get(model) ?? {closed: 0, overlap: 0};
    total.closed += closed;
    total.overlap += overlap;
    totals.set(model, total);
  }
  const models = Array.from(totals).sort((a, b) => b[1].closed - a[1].closed || b[1].overlap - a[1].overlap);
  renderBars("credits", models.map(([model, {closed, overlap}]) => ({
    label: model, segments: [[closed, ""], [overlap, "overlap"]],
    value: overlap ? `${closed} · ${overlap} 重复` : String(closed)
  })), Math.max(...models.map(([, row]) => row.closed + row.overlap)));
  byId("credit-evidence").replaceChildren(...data.credits.slice().reverse().map(row => {
    const item = el("li", `${row.model} · ${showDate(row.date)} · 新增 ${row.closed} 片，重复覆盖 ${row.overlap} 片 · `);
    item.append(link("审阅记录", row.url));
    return item;
  }));

  const histogram = new Map();
  for (const {exponents} of data.shards) {
    if (exponents.length) histogram.set(exponents.length, (histogram.get(exponents.length) ?? 0) + 1);
  }
  const maximum = Math.max(1, ...histogram.values());
  const bins = Array.from(histogram).sort(([a], [b]) => a - b).map(([keys, shards]) => {
    const bin = el("div", "", "bin");
    const track = el("div", "", "bar-track");
    const bar = el("div", "", "bar-fill");
    bar.style.width = 100 * shards / maximum + "%";
    track.append(bar);
    bin.append(el("strong", `${shards} 片`), track, el("span", `余 ${keys} 个指数`));
    return bin;
  });
  byId("distribution").replaceChildren(...(bins.length ? bins : [el("span", "所有分片已闭合")]));
}

function drawTrend() {
  if (!data) return;
  const cutoff = byId("cutoff").value;
  const index = data.history.findIndex(entry => entry.sha === cutoff);
  const visible = index < 0 ? data.history : data.history.slice(0, index + 1);
  const latest = visible.at(-1);
  const canvas = byId("trend-chart");
  const tip = byId("trend-tip");
  tip.hidden = true;
  const width = canvas.clientWidth;
  const height = canvas.clientHeight;
  const ratio = window.devicePixelRatio || 1;
  canvas.width = width * ratio;
  canvas.height = height * ratio;
  const ctx = canvas.getContext("2d");
  ctx.scale(ratio, ratio);
  const left = 49, right = width - 17, top = 28, bottom = height - 30;
  const baseline = Math.floor(Math.min(...visible.map(entry => entry.closed)) / 400) * 400;
  const times = visible.map(entry => +new Date(entry.timestamp));
  const first = Math.min(...times);
  const asOf = index < 0 ? Math.max(...times, +new Date(data.source.timestamp)) : Math.max(...times);
  const x = date => left + (date - first) / Math.max(1, asOf - first) * (right - left);
  const y = count => bottom - (count - baseline) / Math.max(1, data.total - baseline) * (bottom - top);
  trendPoints = visible.map((entry, i) => ({entry, x: x(times[i]), y: y(entry.closed)}));
  const last = trendPoints.at(-1);
  const drawPath = () => {
    let previousY = trendPoints[0].y;
    ctx.moveTo(trendPoints[0].x, previousY);
    for (const point of trendPoints.slice(1)) {
      ctx.lineTo(point.x, previousY);
      ctx.lineTo(point.x, point.y);
      previousY = point.y;
    }
    ctx.lineTo(x(asOf), last.y);
  };
  ctx.font = "12px monospace";
  ctx.fillStyle = "#4f655d";
  ctx.textAlign = "right";
  ctx.textBaseline = "middle";
  const ticks = new Set([data.total]);
  for (let count = baseline; count < data.total - 140; count += 400) ticks.add(count);
  for (const count of ticks) {
    ctx.strokeStyle = "#dbe5e0";
    ctx.beginPath();
    ctx.moveTo(left, y(count));
    ctx.lineTo(right, y(count));
    ctx.stroke();
    ctx.fillText(fmt(count), left - 8, y(count));
  }
  ctx.fillStyle = "#e3f4eb";
  ctx.beginPath();
  drawPath();
  ctx.lineTo(x(asOf), bottom);
  ctx.lineTo(left, bottom);
  ctx.closePath();
  ctx.fill();
  ctx.strokeStyle = "#087253";
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  drawPath();
  ctx.stroke();
  ctx.fillStyle = "#087253";
  for (const point of trendPoints) {
    ctx.beginPath();
    ctx.arc(point.x, point.y, point === last ? 4.5 : 3, 0, 2 * Math.PI);
    ctx.fill();
  }
  const tickCount = asOf === first ? 1 : width < 480 ? 3 : 5;
  for (let i = 0; i < tickCount; i++) {
    const date = first + i / Math.max(1, tickCount - 1) * (asOf - first);
    ctx.textAlign = i === 0 ? "left" : i === tickCount - 1 ? "right" : "center";
    ctx.fillStyle = "#4f655d";
    ctx.fillText(showDate(date).slice(0, 5), x(date), bottom + 19);
  }
  const description = `截至 ${fullDate(asOf)}，闭合 ${fmt(latest.closed)} / ${fmt(data.total)} 片，剩余 ${fmt(data.total - latest.closed)} 片。`;
  byId("trend-summary").textContent = description;
  canvas.setAttribute("aria-label", "累计闭合分片阶梯图。" + description);
  byId("milestones").replaceChildren(...visible.slice().reverse().map(entry => {
    const item = el("li", `${showDate(entry.timestamp)} · ${fmt(entry.closed)} 片 · `);
    item.append(link(entry.label ?? entry.title, entry.url));
    return item;
  }));
}

function renderTable() {
  if (!data) return;
  const query = byId("query").value.trim().toUpperCase();
  const key = query.match(/^(\d+)\s*[:,，：^]\s*(\d+)$/);
  const root = byId("root").value;
  const state = byId("state").value;
  const filtered = data.shards.filter(shard => {
    const open = shard.exponents.length > 0;
    if (root && Number(root) !== shard.root) return false;
    if (state && (state === "open") !== open) return false;
    if (key) return shard.root === Number(key[1]) && shard.exponents.includes(Number(key[2]));
    return shard.id.includes(query) || shard.exponents.some(e => String(e) === query);
  });
  const last = Math.max(0, Math.ceil(filtered.length / pageSize) - 1);
  page = Math.min(page, last);
  const rows = filtered.slice(page * pageSize, (page + 1) * pageSize).map(shard => {
    const row = el("tr");
    const open = shard.exponents.length > 0;
    row.append(el("td", shard.id), el("td", shard.root),
      el("td", open ? "开放" : "闭合", open ? "state-open" : "state-closed"),
      el("td", open ? shard.exponents.join(" · ") : "—"));
    return row;
  });
  if (!rows.length) {
    const cell = el("td", "没有符合条件的分片");
    cell.colSpan = 4;
    const row = el("tr");
    row.append(cell);
    rows.push(row);
  }
  byId("shard-rows").replaceChildren(...rows);
  byId("table-count").textContent = `共 ${fmt(filtered.length)} 片 · 第 ${page + 1} / ${last + 1} 页`;
  byId("prev").disabled = page === 0;
  byId("next").disabled = page === last;
}

async function refresh() {
  try {
    const response = await fetch("data.json", {cache: "no-store"});
    if (!response.ok) throw new Error("HTTP " + response.status);
    const update = await response.json();
    byId("notice").hidden = true;
    if (data?.source.sha === update.source.sha) return;
    const cutoff = byId("cutoff").value;
    const root = byId("root").value;
    data = update;
    const projectStatus = byId("project-status");
    projectStatus.textContent = ({
      INCOMPLETE_FRONTIER: "全局下界待证",
      PROVED: "全局下界已证"
    })[data.status] ?? `账本状态 · ${data.status}`;
    projectStatus.classList.toggle("complete", data.status === "PROVED");
    byId("snapshot").replaceChildren(`截至 ${fullDate(data.source.timestamp)} UTC+8 · `,
      link(data.source.sha.slice(0, 7), data.source.url));
    byId("source").href = data.source.url;
    byId("source").textContent = "查看主线快照";
    byId("ledger").href = data.ledgerUrl;
    byId("cutoff").replaceChildren(new Option("最新主线", ""),
      ...data.history.slice().reverse().map(entry => new Option(fullDate(entry.timestamp), entry.sha)));
    if (data.history.some(entry => entry.sha === cutoff)) byId("cutoff").value = cutoff;
    byId("root").replaceChildren(new Option("全部", ""),
      ...data.roots.map(row => new Option(String(row.root), String(row.root))));
    byId("root").value = root;
    byId("dashboard").hidden = false;
    renderMetrics();
    renderBreakdowns();
    drawTrend();
    renderTable();
  } catch (error) {
    byId("notice").hidden = false;
    byId("notice").textContent = data ? "暂时无法刷新，当前显示上一次成功读取的数据。" : "暂时无法读取主线账本，请稍后刷新。";
    if (!data) byId("project-status").textContent = "数据暂不可用";
    console.error(error);
  }
}

for (const [id, event] of [["query", "input"], ["root", "change"], ["state", "change"]]) {
  byId(id).addEventListener(event, () => { page = 0; renderTable(); });
}
byId("prev").addEventListener("click", () => { page--; renderTable(); });
byId("next").addEventListener("click", () => { page++; renderTable(); });
byId("cutoff").addEventListener("change", drawTrend);
new ResizeObserver(drawTrend).observe(byId("trend-plot"));
byId("trend-chart").addEventListener("pointermove", event => {
  const tip = byId("trend-tip");
  const canvas = event.currentTarget;
  const bounds = canvas.getBoundingClientRect();
  const x = event.clientX - bounds.left;
  const y = event.clientY - bounds.top;
  const point = trendPoints.slice().sort((a, b) =>
    Math.hypot(a.x - x, a.y - y) - Math.hypot(b.x - x, b.y - y))[0];
  if (!point) return;
  tip.textContent = `${showDate(point.entry.timestamp)} · ${fmt(point.entry.closed)} 片`;
  tip.hidden = false;
  tip.style.left = Math.max(0, Math.min(point.x - tip.offsetWidth / 2, canvas.clientWidth - tip.offsetWidth)) + "px";
});
byId("trend-chart").addEventListener("pointerleave", () => { byId("trend-tip").hidden = true; });
document.addEventListener("visibilitychange", () => { if (!document.hidden) refresh(); });
setInterval(() => { if (!document.hidden) refresh(); }, 60_000);
refresh();
