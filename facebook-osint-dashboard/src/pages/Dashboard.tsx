import React, { useState, useEffect } from 'react';
import SearchBar from '../components/Search/SearchBar';
import ScraperStatus from '../components/Status/ScraperStatus';
import DataFeed from '../components/DataViewer/DataFeed';
import NetworkGraph from '../components/Network/NetworkGraph';
import { ScrapedPost, ScraperStatus as ScraperStatusType, NetworkNode, NetworkLink, DashboardStats } from '../types';
import apiService from '../services/api';

const Dashboard: React.FC = () => {
  const [currentView, setCurrentView] = useState<'search' | 'status' | 'data' | 'network'>('search');
  const [posts, setPosts] = useState<ScrapedPost[]>([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState<DashboardStats>({
    totalPosts: 0,
    totalComments: 0,
    totalReactions: 0,
    activeScrapers: 0,
    errorsToday: 0,
    dataCollectedToday: 0,
  });

  const [scraperStatus, setScraperStatus] = useState<ScraperStatusType | null>(null);
  const [networkData, setNetworkData] = useState<{ nodes: NetworkNode[], links: NetworkLink[] }>({ nodes: [], links: [] });

  useEffect(() => {
    // Load initial dashboard stats and data
    const loadInitialData = async () => {
      try {
        // Load dashboard stats
        const statsResponse = await apiService.getDashboardStats();
        if (statsResponse.success && statsResponse.data) {
          setStats(statsResponse.data);
        }

        // Load scraper status
        const statusResponse = await apiService.getScraperStatus();
        if (statusResponse.success && statusResponse.data) {
          setScraperStatus(statusResponse.data);
        }

        // Load network data
        const networkResponse = await apiService.getNetworkGraph();
        if (networkResponse.success && networkResponse.data) {
          setNetworkData({
            nodes: networkResponse.data.nodes || [],
            links: networkResponse.data.links || []
          });
        }
      } catch (error) {
        console.error('Failed to load initial data:', error);
      }
    };

    loadInitialData();

    // Real-time data updates
    const interval = setInterval(async () => {
      try {
        const statsResponse = await apiService.getDashboardStats();
        if (statsResponse.success && statsResponse.data) {
          setStats(statsResponse.data);
        }

        const statusResponse = await apiService.getScraperStatus();
        if (statusResponse.success && statusResponse.data) {
          setScraperStatus(statusResponse.data);
        }
      } catch (error) {
        console.error('Failed to update data:', error);
      }
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  const handleSearch = async (query: string, type: string) => {
    setLoading(true);
    setCurrentView('data');
    
    try {
      // Trigger scraper for keyword
      if (type === 'keyword') {
        await apiService.scrapeByKeyword(query);
      }
      
      // Get posts by keyword
      const response = await apiService.getPostsByKeyword(query);
      if (response.success && response.data) {
        setPosts(response.data.content || response.data);
      } else {
        console.error('Failed to fetch posts:', response.message);
        setPosts([]);
      }
    } catch (error) {
      console.error('Search failed:', error);
      setPosts([]);
    } finally {
      setLoading(false);
    }
  };

  const renderContent = () => {
    switch (currentView) {
      case 'search':
        return (
          <div className="p-6">
            <SearchBar onSearch={handleSearch} />
          </div>
        );
      case 'status':
        return (
          <div className="p-6">
            <ScraperStatus status={scraperStatus} onRefresh={async () => {
              try {
                const response = await apiService.getScraperStatus();
                if (response.success && response.data) {
                  setScraperStatus(response.data);
                }
              } catch (error) {
                console.error('Failed to refresh scraper status:', error);
              }
            }} />
          </div>
        );
      case 'data':
        return (
          <div className="p-6">
            <div className="mb-6">
              <h2 className="text-xl font-semibold text-white mb-2">Scraped Data</h2>
              <p className="text-gray-400">Showing results from recent searches</p>
            </div>
            <DataFeed posts={posts} loading={loading} />
          </div>
        );
      case 'network':
        return (
          <div className="p-6">
            <NetworkGraph 
              nodes={networkData.nodes} 
              links={networkData.links} 
              onLoadNetwork={async (keyword?: string) => {
                try {
                  const response = await apiService.getNetworkGraph(keyword);
                  if (response.success && response.data) {
                    setNetworkData({
                      nodes: response.data.nodes || [],
                      links: response.data.links || []
                    });
                  }
                } catch (error) {
                  console.error('Failed to load network data:', error);
                }
              }}
            />
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* Stats Bar */}
      <div className="bg-dark-surface border-b border-dark-border px-6 py-3">
        <div className="grid grid-cols-6 gap-4 text-center">
          <div>
            <p className="text-lg font-bold text-white">{stats.totalPosts}</p>
            <p className="text-xs text-gray-400">Total Posts</p>
          </div>
          <div>
            <p className="text-lg font-bold text-white">{stats.totalComments}</p>
            <p className="text-xs text-gray-400">Comments</p>
          </div>
          <div>
            <p className="text-lg font-bold text-white">{stats.totalReactions}</p>
            <p className="text-xs text-gray-400">Reactions</p>
          </div>
          <div>
            <p className="text-lg font-bold text-accent-green">{stats.activeScrapers}</p>
            <p className="text-xs text-gray-400">Active Scrapers</p>
          </div>
          <div>
            <p className="text-lg font-bold text-accent-red">{stats.errorsToday}</p>
            <p className="text-xs text-gray-400">Errors Today</p>
          </div>
          <div>
            <p className="text-lg font-bold text-accent-blue">{stats.dataCollectedToday}</p>
            <p className="text-xs text-gray-400">Data Collected</p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden">
        {renderContent()}
      </div>
    </div>
  );
};

export default Dashboard;