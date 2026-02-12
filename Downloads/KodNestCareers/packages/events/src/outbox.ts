// Outbox pattern abstractions will be implemented here.

export interface OutboxEvent {
  id: string;
  type: string;
  payload: unknown;
}

export function enqueueOutboxEvent(_event: OutboxEvent): void {
  // Implement enqueue logic later.
}

