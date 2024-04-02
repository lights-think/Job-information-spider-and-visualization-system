# 工作信息爬虫及可视化系统 Job Information Spider and Visualization System

## 简介 Introduction

这个系统是一个综合解决方案，旨在以用户友好和交互式的方式聚合和显示工作市场数据。利用Python进行网络爬虫，使用Flask作为Web应用框架，以及通过Pyecharts进行动态数据可视化，本系统提供实时的工作趋势、薪资范围和雇主统计信息。后端数据库使用SQLite3，确保高效的数据管理和检索。

This system is a comprehensive solution designed to aggregate and display job market data in a user-friendly and interactive manner. Utilizing Python for web scraping, Flask as the web application framework, and Pyecharts for dynamic data visualization, this system provides real-time insights into job trends, salary ranges, and employer statistics. The backend database, powered by SQLite3, ensures efficient data management and retrieval.

## 主要特性 Key Features

- **数据收集 Data Collection**: 使用Python自动化网页爬虫脚本从多个在线门户收集职位列表和详细信息。
- **Web应用 Web Application**: 基于Flask的界面，允许用户无缝查询和与收集的数据进行交互。
- **数据可视化 Data Visualization**: 集成Pyecharts来创建交互式图表，直观表示工作市场分析。
- **数据库管理 Database Management**: 利用SQLite3高效地存储、组织和访问工作数据。

## 使用的技术 Technologies Used

- **Python网页爬虫 Python Web Scraping**: 使用BeautifulSoup或Scrapy等库提取工作信息。
- **Flask**: 用于服务数据和渲染前端的轻量级WSGI Web应用框架。
- **Pyecharts**: 一个生成交互式且吸引人的图表的Python库。
- **SQLite3**: 提供轻量级磁盘数据库的C库，不需要单独的服务器进程。

## 安装和设置 Installation and Setup

1. 克隆仓库 Clone the repository:
   ```
   git clone https://github.com/yourusername/job-info-spider-visualization.git
   ```
2. 转到项目目录 Navigate to the project directory:
   ```
   cd job-info-spider-visualization
   ```
3. 安装所需依赖 Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. 运行Flask应用 Run the Flask application:
   ```
   flask run
   ```

## 使用方法 Usage

启动Flask服务器后，通过Web浏览器访问`http://127.0.0.1:5000`以使用应用程序。使用界面根据您的标准搜索、筛选和可视化工作市场数据。

After starting the Flask server, navigate to `http://127.0.0.1:5000` in your web browser to access the application. Use the interface to search, filter, and visualize the job market data based on your criteria.

## 贡献 Contributing

欢迎贡献！对于重大变更，请先开一个issue讨论您希望进行的更改。适当地更新测试也是必要的。

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change. Ensure to update tests as appropriate.

## 许可证 License

[MIT](https://choosealicense.com/licenses/mit/)
