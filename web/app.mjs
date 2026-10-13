import { calculateTdi } from './kinetics.mjs';

const form = document.getElementById('kinetics-form');
const error = document.getElementById('form-error');
const result = document.getElementById('result');
const svg = document.getElementById('activity-plot');
let latest = null;

const number = id => {
  const el = document.getElementById(id);
  if (!el.value.trim() || !el.checkValidity()) {
    throw new RangeError('Enter a valid nonnegative value for ' + el.labels[0].textContent.trim());
  }
  const value = Number(el.value);
  if (!Number.isFinite(value)) throw new RangeError('Values must be finite');
  return value;
};
const fmt = n => Number(n).toLocaleString('en-US', { maximumSignificantDigits: 5 });
const ns = 'http://www.w3.org/2000/svg';
const element = (name, props, text) => {
  const el = document.createElementNS(ns, name);
  for (const [key, value] of Object.entries(props)) el.setAttribute(key, value);
  if (text !== undefined) el.textContent = text;
  return el;
};

function plot(kinact, ki, inhibitor, minutes) {
  const width = 680, height = 230, left = 56, top = 14, right = 20, bottom = 36;
  const chartW = width - left - right, chartH = height - top - bottom;
  const end = Math.max(1, minutes);
  svg.replaceChildren();
  svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
  svg.append(element('title', {}, 'Predicted enzyme activity as a function of exposure time'));
  for (let i = 0; i <= 4; i++) {
    const value = i * 25;
    const y = top + chartH * (1 - value / 100);
    svg.append(element('line', { x1: left, x2: width - right, y1: y, y2: y, stroke: '#334155', 'stroke-width': 1 }));
    svg.append(element('text', { x: left - 9, y: y + 4, fill: '#b9c6d8', 'text-anchor': 'end', 'font-size': 12 }, value + '%'));
  }
  for (let i = 0; i <= 4; i++) {
    const x = left + chartW * i / 4;
    svg.append(element('text', { x, y: height - 10, fill: '#b9c6d8', 'text-anchor': 'middle', 'font-size': 12 }, fmt(end * (i / 4))));
  }
  let data = '';
  for (let i = 0; i <= 100; i++) {
    const t = end * (i / 100);
    const y = calculateTdi(kinact, ki, inhibitor, t).activity;
    data += (i === 0 ? 'M' : 'L') + (left + chartW * i / 100).toFixed(2) + ',' + (top + chartH * (1 - y / 100)).toFixed(2) + ' ';
  }
  svg.append(element('path', { d: data.trim(), fill: 'none', stroke: '#60a5fa', 'stroke-width': 3, 'stroke-linejoin': 'round' }));
  svg.append(element('text', { x: left + chartW / 2, y: height - 1, fill: '#b9c6d8', 'text-anchor': 'middle', 'font-size': 11 }, 'Preincubation time (min)'));
}

function calculate(event) {
  if (event) event.preventDefault();
  error.textContent = '';
  try {
    const kinact = number('kinact'), ki = number('ki');
    const inhibitor = number('inhibitor'), minutes = number('minutes');
    const data = calculateTdi(kinact, ki, inhibitor, minutes);
    latest = { kinact, ki, inhibitor, minutes, data };
    document.getElementById('kobs').textContent = fmt(data.kobs) + ' min⁻¹';
    document.getElementById('activity').textContent = fmt(data.activity) + '%';
    document.getElementById('half-life').textContent = data.halfLife === null ? 'Not defined' : fmt(data.halfLife) + ' min';
    document.getElementById('efficiency').textContent = fmt(data.efficiency) + ' µM⁻¹ min⁻¹';
    result.hidden = false;
    document.getElementById('export').disabled = false;
    plot(kinact, ki, inhibitor, minutes);
  } catch (e) {
    latest = null;
    result.hidden = true;
    document.getElementById('export').disabled = true;
    error.textContent = e.message;
  }
}

form.addEventListener('submit', calculate);
document.getElementById('export').addEventListener('click', () => {
  if (!latest) return;
  const { kinact, ki, inhibitor, minutes } = latest;
  const csv = ['time_min,inhibitor_um,kinact_per_min,ki_um,kobs_per_min,remaining_activity_pct'];
  for (let i = 0; i <= 100; i++) {
    const time = minutes * (i / 100);
    const r = calculateTdi(kinact, ki, inhibitor, time);
    csv.push([time, inhibitor, kinact, ki, r.kobs, r.activity].join(','));
  }
  const url = URL.createObjectURL(new Blob([csv.join('\n') + '\n'], { type: 'text/csv;charset=utf-8' }));
  const link = document.createElement('a');
  link.href = url;
  link.download = 'cyp-tdi-model.csv';
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
calculate();
