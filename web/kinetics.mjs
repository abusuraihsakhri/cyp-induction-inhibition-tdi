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
  const kobs = kinact * inhibitor / (ki + inhibitor);
  return {
    kobs,
    activity: 100 * Math.exp(-kobs * minutes),
    halfLife: kobs > 0 ? Math.LN2 / kobs : null,
    efficiency: kinact / ki
  };
}
