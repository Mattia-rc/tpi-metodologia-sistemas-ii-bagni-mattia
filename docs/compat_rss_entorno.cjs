// Local runner workaround: the sandbox denies the OS RSS query used by Angular telemetry.
// Does not alter compilation or application code. Not part of the delivered application.
const v8 = require('node:v8');
const real = process.memoryUsage.bind(process);
function usage() {
  try { return real(); }
  catch (error) {
    if (error.code !== 'ENOENT') throw error;
    const heap = v8.getHeapStatistics();
    return {rss: 0, heapTotal: heap.total_heap_size, heapUsed: heap.used_heap_size, external: heap.external_memory, arrayBuffers: 0};
  }
}
usage.rss = () => usage().rss;
process.memoryUsage = usage;
