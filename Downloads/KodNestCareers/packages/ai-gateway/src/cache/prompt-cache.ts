// Simple in memory prompt cache placeholder.

export interface PromptCacheEntry {
  key: string;
  value: string;
}

export class PromptCache {
  private entries: PromptCacheEntry[] = [];

  add(entry: PromptCacheEntry): void {
    this.entries.push(entry);
  }
}

