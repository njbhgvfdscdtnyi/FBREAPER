const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8080/api';

export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

class ApiService {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${API_BASE_URL}${endpoint}`;
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || `HTTP error! status: ${response.status}`);
      }
      
      return { data, success: true };
    } catch (error) {
      console.error('API request failed:', error);
      return {
        data: null as T,
        success: false,
        message: error instanceof Error ? error.message : 'Unknown error occurred',
      };
    }
  }

  // Scraper endpoints
  async startScraper(): Promise<ApiResponse<string>> {
    return this.request<string>('/scraper/start', { method: 'POST' });
  }

  async scrapeByKeyword(keyword: string): Promise<ApiResponse<string>> {
    return this.request<string>(`/scraper/scrapeByKeyword?keyword=${encodeURIComponent(keyword)}`, {
      method: 'POST',
    });
  }

  async getScraperStatus(): Promise<ApiResponse<any>> {
    return this.request<any>('/scraper/status');
  }

  // Data endpoints
  async getPosts(page: number = 0, size: number = 20): Promise<ApiResponse<any>> {
    return this.request<any>(`/data/posts?page=${page}&size=${size}`);
  }

  async getPostsByKeyword(keyword: string, page: number = 0, size: number = 20): Promise<ApiResponse<any>> {
    return this.request<any>(`/data/posts/search?keyword=${encodeURIComponent(keyword)}&page=${page}&size=${size}`);
  }

  async getComments(postId: string, page: number = 0, size: number = 20): Promise<ApiResponse<any>> {
    return this.request<any>(`/data/posts/${postId}/comments?page=${page}&size=${size}`);
  }

  // Network analysis endpoints
  async getNetworkGraph(keyword?: string): Promise<ApiResponse<any>> {
    const endpoint = keyword 
      ? `/network/graph?keyword=${encodeURIComponent(keyword)}`
      : '/network/graph';
    return this.request<any>(endpoint);
  }

  async getLinkAnalysis(url: string): Promise<ApiResponse<any>> {
    return this.request<any>(`/network/link-analysis?url=${encodeURIComponent(url)}`);
  }

  // Dashboard stats
  async getDashboardStats(): Promise<ApiResponse<any>> {
    return this.request<any>('/data/stats');
  }

  // Health check
  async getHealth(): Promise<ApiResponse<any>> {
    return this.request<any>('/health');
  }
}

export const apiService = new ApiService();
export default apiService;