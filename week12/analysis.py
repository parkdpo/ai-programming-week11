from pathlib import Path

import pandas as pd


def 정제(df):
	정제본 = df.copy(deep=True)

	# 점수가 비어 있는 행을 삭제한다.
	정제본 = 정제본.dropna(subset=["점수"])
	print(f"점수 결측 행 삭제 후: {len(정제본)}행")

	# 모든 열이 같은 중복 행을 하나만 남긴다.
	정제본 = 정제본.drop_duplicates()
	print(f"중복 행 삭제 후: {len(정제본)}행")

	# 반과 과목의 앞뒤 공백을 제거한다.
	정제본["반"] = 정제본["반"].str.strip()
	정제본["과목"] = 정제본["과목"].str.strip()
	print(f"공백 제거 후: {len(정제본)}행")

	# 점수가 0에서 100 사이가 아닌 행을 삭제한다.
	정제본 = 정제본[정제본["점수"].between(0, 100)]
	print(f"점수 범위 정리 후: {len(정제본)}행")

	return 정제본


df = pd.read_csv(Path(__file__).with_name("scores_2026.csv"))
df = 정제(df)
print(df.shape)# (114, 5)
print(df["점수"].isna().sum()) # 6      ← 빈 칸이 몇 개인가
print(df.duplicated().sum()) # 4      ← 완전히 같은 행이 몇 개인가
print(df["반"].unique()) # ['2반' '1반' '1반 ']      ← 세 개?
print(df["과목"].unique()) # ['수학' '프로그래밍' '영어' '프로그래밍 ']
print(df["점수"].describe()) # max 999.0  min -5.0   ← 점수인데?

# 반별 점수 평균을 계산한다.
반별_평균 = df.groupby("반")["점수"].mean()
print("반별 점수 평균:")
print(반별_평균)

# 과목과 반별 점수 평균을 계산한다.
과목_반별_평균 = df.groupby(["과목", "반"])["점수"].mean()
print("과목과 반별 점수 평균:")
print(과목_반별_평균)

# 반별 점수 개수, 평균, 중앙값, 최댓값을 표로 계산한다.
반별_통계 = df.groupby("반").agg(
	개수=("점수", "count"),
	평균=("점수", "mean"),
	중앙값=("점수", "median"),
	최댓값=("점수", "max"),
).round(2)
print("반별 점수 통계:")
print(반별_통계)

