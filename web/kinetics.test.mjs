import test from 'node:test';
import assert from 'node:assert/strict';
import { calculateTdi } from './kinetics.mjs';

const close = (actual, expected, tol = 1e-10) =>
  assert.ok(Math.abs(actual - expected) < tol, `${actual} != ${expected}`);

test('TDI model matches independent analytical values', () => {
  const r = calculateTdi(0.2, 5, 5, 10);
  close(r.kobs, 0.1);
  close(r.activity, 100 * Math.exp(-1));
  close(r.halfLife, Math.LN2 / 0.1);
  close(r.efficiency, 0.04);
});
test('zero inhibitor and zero inactivation preserve enzyme activity', () => {
  assert.equal(calculateTdi(0.2, 5, 0, 10).activity, 100);
  assert.equal(calculateTdi(0, 5, 5, 10).halfLife, null);
});
test('invalid and non-finite kinetics are rejected', () => {
  for (const values of [[-1, 5, 5, 10], [0.2, 0, 5, 10], [0.2, 5, -5, 10],
    [0.2, 5, 5, -1], [NaN, 5, 5, 10], [0.2, Infinity, 5, 10]]) {
    assert.throws(() => calculateTdi(...values), RangeError);
  }
});
