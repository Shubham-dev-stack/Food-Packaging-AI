/**
 * Typed HTTP API client for Food Packaging AI Backend.
 * Uses Vite proxy (/api) in development and respects canonical /api prefix.
 */

import type {
  ApiErrorResponse,
  CommodityBriefResponse,
  CommodityDetailResponse,
  EvidenceSourceResponse,
  RecommendationCreateRequest,
  RecommendationResponse,
} from '../types/api';

const evidenceCache = new Map<string, EvidenceSourceResponse>();

export class ApiError extends Error {
  public readonly status: number;
  public readonly response: ApiErrorResponse;

  constructor(status: number, response: ApiErrorResponse) {
    super(response.message || `API Request failed with HTTP ${status}`);
    this.name = 'ApiError';
    this.status = status;
    this.response = response;
  }
}

export const DEFAULT_REQUEST_TIMEOUT_MS = 10000;

async function request<T>(
  endpoint: string,
  options?: RequestInit & { timeoutMs?: number },
): Promise<T> {
  const url = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;

  const defaultHeaders: Record<string, string> = {
    Accept: 'application/json',
  };

  if (options?.body) {
    defaultHeaders['Content-Type'] = 'application/json';
  }

  const timeoutMs = options?.timeoutMs ?? DEFAULT_REQUEST_TIMEOUT_MS;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  let response: Response;
  try {
    response = await fetch(url, {
      ...options,
      signal: options?.signal || controller.signal,
      headers: {
        ...defaultHeaders,
        ...options?.headers,
      },
    });
  } catch (err: unknown) {
    clearTimeout(timeoutId);
    if (err instanceof DOMException && err.name === 'AbortError') {
      throw new ApiError(408, {
        error: 'REQUEST_TIMEOUT',
        message: `Request timed out after ${timeoutMs}ms. Please check your backend connection and try again.`,
        details: [],
      });
    }
    throw new ApiError(0, {
      error: 'NETWORK_ERROR',
      message: err instanceof Error ? err.message : 'Network error connecting to backend service.',
      details: [],
    });
  } finally {
    clearTimeout(timeoutId);
  }

  if (!response.ok) {
    let errorData: ApiErrorResponse;
    try {
      errorData = await response.json();
    } catch {
      errorData = {
        error: 'NETWORK_ERROR',
        message: `HTTP error ${response.status}: ${response.statusText}`,
        details: [],
      };
    }
    throw new ApiError(response.status, errorData);
  }

  return response.json() as Promise<T>;
}

export const api = {
  /**
   * Retrieve all supported commodities in the knowledge base, optionally filtered by category.
   */
  async getCommodities(category?: string): Promise<CommodityBriefResponse[]> {
    const query = category ? `?category=${encodeURIComponent(category)}` : '';
    return request<CommodityBriefResponse[]>(`/api/commodities${query}`);
  },

  /**
   * Retrieve detailed postharvest physicochemical and respiration parameters for a specific commodity.
   */
  async getCommodity(commodityId: string): Promise<CommodityDetailResponse> {
    return request<CommodityDetailResponse>(`/api/commodities/${encodeURIComponent(commodityId)}`);
  },

  /**
   * Evaluate optimal packaging materials and technical specifications for given food commodity context.
   */
  async createRecommendation(payload: RecommendationCreateRequest): Promise<RecommendationResponse> {
    return request<RecommendationResponse>('/api/recommendations', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  /**
   * Retrieve a previously evaluated recommendation audit session by request ID.
   */
  async getRecommendation(requestId: string): Promise<RecommendationResponse> {
    return request<RecommendationResponse>(`/api/recommendations/${encodeURIComponent(requestId)}`);
  },

  /**
   * Retrieve evidence source by reference ID with in-memory session caching.
   */
  async getEvidence(referenceId: string): Promise<EvidenceSourceResponse> {
    if (evidenceCache.has(referenceId)) {
      return evidenceCache.get(referenceId)!;
    }
    const data = await request<EvidenceSourceResponse>(`/api/evidence/${encodeURIComponent(referenceId)}`);
    evidenceCache.set(referenceId, data);
    return data;
  },

  /**
   * Retrieve all bibliographic evidence sources.
   */
  async getEvidenceList(): Promise<EvidenceSourceResponse[]> {
    const list = await request<EvidenceSourceResponse[]>('/api/evidence');
    list.forEach((item) => evidenceCache.set(item.reference_id, item));
    return list;
  },

  /**
   * Health status check.
   */
  async checkHealth(): Promise<{ status: string; service: string; version: string }> {
    return request<{ status: string; service: string; version: string }>('/api/health');
  },
};
