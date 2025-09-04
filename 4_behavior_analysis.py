import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pyhive import hive
from thrift.transport.TTransport import TTransportException


def create_hive_connection(host, port, database, username):
    """创建Hive连接"""
    try:
        conn = hive.Connection(
            host=host,
            port=port,
            database=database,
            username=username,
            auth='NONE'  # 使用NONE认证方式
        )
        print("✅ Hive连接成功")
        return conn
    except TTransportException:
        print("❌ Hive连接失败：请检查HiveServer2是否启动，IP和端口是否正确")
        print("   启动HiveServer2命令：hive --service hiveserver2 &")
        return None
    except Exception as e:
        print(f"❌ 连接出错：{str(e)}")
        return None


def fetch_repurchase_data(conn):
    """从Hive获取复购率数据"""
    if not conn:
        return None, None

    try:
        # 创建游标
        cursor = conn.cursor()

        # 1. 获取整体复购率
        overall_sql = """
        SELECT (COUNT(DISTINCT r.user_id) / COUNT(DISTINCT n.user_id)) * 100 
        AS repurchase_rate FROM nov_buy_users n
        LEFT JOIN repurchase_users r ON n.user_id = r.user_id
        """
        cursor.execute(overall_sql)
        overall_rate = cursor.fetchone()[0]
        print(f"📊 整体复购率：{overall_rate:.2f}%")

        # 2. 获取分品类复购率
        category_sql = """
        SELECT t1.category_id,
               (COUNT(DISTINCT t2.user_id) / COUNT(DISTINCT t1.user_id)) * 100 
               AS category_repurchase
        FROM (
            SELECT DISTINCT user_id, category_id
            FROM user_behavior
            WHERE month = 11 AND behavior_type = 'buy'
        ) t1
        LEFT JOIN (
            SELECT DISTINCT user_id, category_id
            FROM user_behavior
            WHERE month = 12 AND behavior_type = 'buy'
        ) t2 ON t1.user_id = t2.user_id AND t1.category_id = t2.category_id
        GROUP BY t1.category_id
        ORDER BY category_repurchase DESC
        """
        cursor.execute(category_sql)
        category_data = cursor.fetchall()
        category_df = pd.DataFrame(
            category_data,
            columns=['category_id', 'repurchase_rate']
        )
        print(f"📊 分品类数据行数：{len(category_df)}")

        cursor.close()
        return overall_rate, category_df

    except Exception as e:
        print(f"❌ 数据查询出错：{str(e)}")
        return None, None


def set_matplotlib_font():
    """设置matplotlib字体，解决中文显示问题"""
    try:
        # 强制使用微软雅黑字体（Windows系统默认存在）
        plt.rcParams["font.family"] = ["Microsoft YaHei"]
        plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
        return True
    except:
        print("⚠️ 系统中未找到微软雅黑字体，图表中文可能显示异常")
        return False


def plot_repurchase_charts(overall_rate, category_df):
    """生成复购率可视化图表，动态设置Y轴范围确保柱子可见"""
    if overall_rate is None:
        print("⚠️ 没有可用的整体复购率数据")
        return

    # 设置字体
    set_matplotlib_font()

    # 1. 整体复购率柱状图
    plt.figure(figsize=(8, 5))
    plt.bar(['11月购买用户12月复购率'], [overall_rate], color='skyblue')
    plt.title('整体复购率', fontsize=15)
    plt.ylabel('复购率 (%)', fontsize=12)
    # 动态设置Y轴范围（整体复购率）
    y_max = max(0.5, overall_rate * 1.5)  # 至少0.5%的范围，确保柱子可见
    plt.ylim(0, y_max)
    plt.text(0, overall_rate + y_max * 0.05, f'{overall_rate:.2f}%', ha='center')
    plt.tight_layout()
    plt.savefig('overall_repurchase_rate.png', dpi=300)
    print("💾 整体复购率图表已保存为 overall_repurchase_rate.png")

    # 2. 分品类复购率柱状图
    if category_df is not None and not category_df.empty:
        plt.figure(figsize=(12, 6))
        # 只显示前10个品类，避免图表过挤
        top_categories = category_df.head(10)
        bars = plt.bar(
            top_categories['category_id'].astype(str),
            top_categories['repurchase_rate'],
            color='lightgreen'
        )
        plt.title('分品类复购率（前10名）', fontsize=15)
        plt.xlabel('品类ID', fontsize=12)
        plt.ylabel('复购率 (%)', fontsize=12)
        plt.xticks(rotation=45)  # 旋转X轴标签，避免重叠

        # 动态设置Y轴范围（分品类复购率）
        max_rate = top_categories['repurchase_rate'].max()
        # 确保Y轴范围至少为0.5%，或数据最大值的1.2倍（取较大值）
        y_max_cat = max(0.5, max_rate * 1.2) if max_rate > 0 else 0.5
        plt.ylim(0, y_max_cat)

        # 在柱子上方显示具体数值
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2., height + y_max_cat * 0.02,
                     f'{height:.2f}%', ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        plt.savefig('category_repurchase_rate.png', dpi=300)
        print("💾 分品类复购率图表已保存为 category_repurchase_rate.png")
    else:
        print("⚠️ 没有可用的分品类复购率数据，不生成分品类图表")


if __name__ == "__main__":
    # ==================== 请修改为你的Hive配置 ====================
    HIVE_HOST = "192.168.88.161"  # 替换为你的Linux虚拟机IP
    HIVE_PORT = 10000  # HiveServer2默认端口
    HIVE_DB = "ecommerce_db"  # 数据库名
    HIVE_USER = "root"  # Linux用户名
    # ============================================================

    # 1. 连接Hive
    conn = create_hive_connection(HIVE_HOST, HIVE_PORT, HIVE_DB, HIVE_USER)

    # 2. 获取复购率数据
    overall_rate, category_df = fetch_repurchase_data(conn)

    # 3. 生成可视化图表
    plot_repurchase_charts(overall_rate, category_df)

    # 4. 关闭连接
    if conn:
        conn.close()
    print("✅ 程序执行完毕")
