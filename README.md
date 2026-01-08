# 코딩 테스트 문제 풀이

코딩 테스트 문제를 풀고 정리한 내용을 저장하기 위한 저장소입니다.

## 📁 폴더 구조

```
├── BFS/          # 너비 우선 탐색 (Breadth First Search)
├── DFS/          # 깊이 우선 탐색 (Depth First Search)
├── Simulation/   # 시뮬레이션
└── ...           # 추가 자료구조/알고리즘
```

## 🔄 Notion 자동 동기화

이 저장소는 Notion에서 정리한 문제 풀이를 자동으로 가져와 GitHub에 업로드합니다.

### 사용법

```bash
./sync.sh           # 전체 동기화 (Notion → Local → GitHub)
./sync.sh pull      # Notion에서만 가져오기
./sync.sh push      # GitHub에만 push
./sync.sh status    # 현재 상태 확인
```

### 동작 방식

1. Notion API를 통해 문제 풀이 페이지들을 가져옴
2. Heading 블록을 기준으로 자료구조/알고리즘별 폴더에 자동 분류
3. Markdown 파일로 변환하여 저장
4. Git commit 후 GitHub에 자동 push
