# Facebook OSINT Dashboard

A polished, desktop-focused React dashboard for monitoring Facebook OSINT scraping operations. Built with TypeScript, Tailwind CSS, and modern React patterns.

## Features

### 🎯 Core Functionality
- **Advanced Search**: Search for users, groups, pages, and keywords across Facebook
- **Real-time Monitoring**: Live scraper status with progress tracking and error reporting
- **Data Visualization**: Interactive feed showing scraped posts, comments, and reactions
- **Network Analysis**: Interactive network graph for link analysis with zoom and pan capabilities

### 🎨 Design & UX
- **Dark Theme**: Professional dark interface optimized for long monitoring sessions
- **Responsive Layout**: Desktop-focused design with collapsible sidebar navigation
- **Smooth Animations**: Loading states, transitions, and real-time updates
- **Clean Typography**: JetBrains Mono font for optimal readability

### 📊 Dashboard Components
- **Search Bar**: Multi-type search with quick search suggestions
- **Scraper Status**: Real-time progress indicators, error tracking, and ETA
- **Data Feed**: Scrollable list of scraped posts with user avatars and engagement metrics
- **Network Graph**: Interactive visualization for analyzing connections between entities
- **Statistics Bar**: Live metrics showing total posts, comments, reactions, and more

## Technology Stack

- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Lucide React** for icons
- **Recharts** for data visualization
- **Custom hooks** for state management

## Project Structure

```
src/
├── components/
│   ├── Layout/
│   │   ├── DashboardLayout.tsx
│   │   └── Sidebar.tsx
│   ├── Search/
│   │   └── SearchBar.tsx
│   ├── Status/
│   │   └── ScraperStatus.tsx
│   ├── DataViewer/
│   │   └── DataFeed.tsx
│   └── Network/
│       └── NetworkGraph.tsx
├── pages/
│   └── Dashboard.tsx
├── types/
│   └── index.ts
└── App.tsx
```

## Getting Started

### Prerequisites
- Node.js 16+ 
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd facebook-osint-dashboard
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Open [http://localhost:3000](http://localhost:3000) to view the dashboard

### Building for Production

```bash
npm run build
```

## Usage

### Navigation
- Use the sidebar to switch between different dashboard sections
- Click the toggle button to collapse/expand the sidebar
- Each section provides focused functionality for specific OSINT tasks

### Search Functionality
- Select search type (keyword, user, group, page)
- Enter search terms in the input field
- Use quick search buttons for common queries
- Results are displayed in the Data Viewer section

### Monitoring Scrapers
- View real-time scraper status and progress
- Monitor error logs and estimated completion times
- Track multiple scraper instances simultaneously

### Data Analysis
- Browse scraped posts with full context
- Expand comments to view detailed discussions
- Analyze engagement metrics and user interactions
- Export data for further analysis

### Network Analysis
- Visualize connections between users, groups, and pages
- Filter by entity type for focused analysis
- Zoom and pan through the network graph
- Click nodes for detailed information

## Customization

### Styling
The dashboard uses Tailwind CSS with custom color schemes. Modify `tailwind.config.js` to adjust:
- Color palette
- Typography
- Spacing and layout

### Data Integration
Replace mock data in `Dashboard.tsx` with real API calls:
- Connect to your scraper backend
- Implement WebSocket connections for real-time updates
- Add authentication and user management

### Component Extension
Each component is modular and can be extended:
- Add new search types
- Implement additional visualization charts
- Create custom data filters and exports

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security Notes

- This dashboard is designed for legitimate OSINT research
- Ensure compliance with Facebook's Terms of Service
- Implement proper rate limiting and ethical scraping practices
- Use appropriate authentication and access controls

## Support

For questions or issues, please open an issue on the repository or contact the development team.
