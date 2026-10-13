/** One-site saturable CYP time-dependent inactivation model.
 * Assumes constant [I], fitted k_inact and K_I, first-order loss.
 * It does NOT estimate kinetic parameters or predict clinical DDIs.
 */
export function calculateTdi(kinact, ki, inhibitor, minutes) {
  const values = { kinact, ki, inhibitor, minutes };
  for (const [name, value] of Object.entries(values)) {
    if (typeof value !== 'number' || !Number.isFinite(value) || value < 0) {
      throw new RangeError(name + ' must be a finite nonnegative number');
    }
  }
  if (ki === 0) throw new RangeError('K_I must be greater than zero');
  const x = inhibitor <= ki ? inhibitor / ki : ki / inhibitor;
  const fraction = inhibitor <= ki ? x / (1 + x) : 1 / (1 + x);
  const kobs = kinact * fraction;
  const efficiency = kinact / ki;
  if (!Number.isFinite(efficiency)) throw new RangeError('k_inact/K_I is outside the numeric range');
  const halfLife = kobs > 0 ? Math.LN2 / kobs : null;
  return {
    kobs,
    activity: 100 * Math.exp(-kobs * minutes),
    halfLife: halfLife !== null && Number.isFinite(halfLife) ? halfLife : null,
    efficiency
  };
}
