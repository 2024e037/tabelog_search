import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# グラフの日本語文字化けを防ぐ（授業用のパッケージが入っている前提）
try:
    import japanize_matplotlib
except ImportError:
    pass

# 1. アプリのタイトルと説明
st.title("🍜 金沢ラーメン・カフェ 穴場サーチアプリ")
st.write("「予算」と「評価（星評価・人気度）」のバランスが良いお店を視覚的に探せます！")

# 2. クレンジング済みのデータを読み込む
df = pd.read_csv("tabelog_cleaned.csv")

# 3. サイドバーの絞り込み機能
st.sidebar.header("🔍 絞り込み条件")

# 予算のスライダー
max_price = int(df['price'].max())
min_price = int(df['price'].min())
selected_price = st.sidebar.slider(
    "最大予算 (円)", 
    min_value=min_price, 
    max_value=max_price, 
    value=max_price, 
    step=100
)

# 最小の星評価のスライダー
min_star = float(df['star'].min())
max_star = float(df['star'].max())
selected_star = st.sidebar.slider(
    "最低の星評価 (★)", 
    min_value=min_star, 
    max_value=max_star, 
    value=min_star, 
    step=0.1
)

# 4. データのフィルタリング（スライダーの値に合致するものだけを残す）
filtered_df = df[
    (df['price'] <= selected_price) & 
    (df['star'] >= selected_star)
]

# 5. グラフ（散布図）の描画
st.subheader("📊 コスパ分析（散布図）")
if not filtered_df.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 散布図を描画（X軸：価格、Y軸：人気スコア、点の大きさ：口コミ数、色：星評価）
    sc = ax.scatter(
        filtered_df['price'], 
        filtered_df['pop_score'], 
        c=filtered_df['star'], 
        cmap='Oranges', 
        s=filtered_df['review'] * 5,  # 口コミが多いお店ほど丸が大きくなる
        alpha=0.7, 
        edgecolors='gray'
    )
    
    ax.set_xlabel("予算 (円)", fontsize=12)
    ax.set_ylabel("人気度（pop_score）", fontsize=12)
    ax.set_title("価格 vs 人気度（大きい丸ほど口コミが多い店）", fontsize=14)
    fig.colorbar(sc, label="星評価（★）")
    
    st.pyplot(fig)
else:
    st.warning("条件に一致するお店が見つかりませんでした。スライダーを動かして条件を緩めてみてください。")

# 6. ランキングテーブルの表示
st.subheader("🏆 おすすめ店舗ランキング (人気スコア順)")
if not filtered_df.empty:
    # 人気スコアが高い順に並び替え
    ranking_df = filtered_df.sort_values(by='pop_score', ascending=False)
    
    # 順位を見やすく1から振り直す
    ranking_df = ranking_df.reset_index(drop=True)
    ranking_df.index = ranking_df.index + 1
    
    # 表示する列を絞ってテーブルを表示
    st.dataframe(ranking_df[['name', 'star', 'review', 'price', 'pop_score', 'url']])
else:
    st.write("条件に一致するお店がないため、ランキングを表示できません。")
    import japanize_matplotlib
