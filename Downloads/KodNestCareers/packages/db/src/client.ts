// Placeholder database client wrapper.
// The concrete Prisma client instance will be wired in later.

export interface DbClient {
  // Extend with query helpers when implementing.
}

export function createDbClient(): DbClient {
  return {};
}

