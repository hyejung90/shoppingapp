import re

import streamlit as st

st.set_page_config(page_title="쇼핑 리스트", page_icon="🛒", layout="centered")

# ---------- 스타일 (최소한의 CSS) ----------
st.markdown(
    """
    <style>
    .block-container { max-width: 640px; padding-top: 2.5rem; }
    h1 { font-size: 2rem !important; text-align: center; padding-bottom: 0.25rem; }
    .subtitle { text-align: center; color: #6b7280; margin-bottom: 1.5rem; }
    .empty-state { text-align: center; padding: 2.5rem 1rem; color: #6b7280;
                   background: #eef4ee; border-radius: 12px; }
    .empty-state .emoji { font-size: 3rem; line-height: 1.2; }
    .empty-state .title { font-weight: 600; color: #1f2937; margin-top: 0.5rem; }
    /* 모바일에서도 아이템 행(체크박스+수정+삭제)을 한 줄로 유지 */
    [data-testid="stHorizontalBlock"]:has([data-testid="stCheckbox"]) { flex-wrap: nowrap !important; }
    [data-testid="stHorizontalBlock"]:has([data-testid="stCheckbox"]) > [data-testid="stColumn"] {
        min-width: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- 상태 초기화 ----------
# 주의: "items"는 session_state의 dict 메서드와 충돌하므로 키 이름으로 쓰지 않는다.
if "shopping_items" not in st.session_state:
    st.session_state.shopping_items = []  # 아이템: {id, name, qty, checked}
if "next_id" not in st.session_state:
    st.session_state.next_id = 1
if "editing" not in st.session_state:
    st.session_state.editing = None  # 수정 중인 아이템 id


# ---------- 동작 함수 ----------
def escape_md(text: str) -> str:
    """사용자 입력이 마크다운으로 해석되지 않도록 ASCII 구두점을 이스케이프한다."""
    return re.sub(r"([!-/:-@\[-`{-~])", r"\\\1", text)



def add_item(name: str, qty: int) -> None:
    st.session_state.shopping_items.append(
        {"id": st.session_state.next_id, "name": name, "qty": qty, "checked": False}
    )
    st.session_state.next_id += 1


def update_item(item_id: int, name: str, qty: int) -> None:
    for item in st.session_state.shopping_items:
        if item["id"] == item_id:
            item["name"], item["qty"] = name, qty


def delete_item(item_id: int) -> None:
    st.session_state.shopping_items = [
        i for i in st.session_state.shopping_items if i["id"] != item_id
    ]
    if st.session_state.editing == item_id:
        st.session_state.editing = None


def toggle_item(item_id: int) -> None:
    # 체크박스 위젯 값(chk_{id})을 아이템 데이터에 반영
    for item in st.session_state.shopping_items:
        if item["id"] == item_id:
            item["checked"] = st.session_state[f"chk_{item_id}"]


def clear_checked() -> None:
    st.session_state.shopping_items = [
        i for i in st.session_state.shopping_items if not i["checked"]
    ]
    st.session_state.editing = None


# ---------- 화면 ----------
st.title("🛒 쇼핑 리스트")
st.markdown('<div class="subtitle">살 것을 적고, 담으면 체크하세요</div>', unsafe_allow_html=True)

# 추가 폼 영역 (F1)
with st.form("add_form", clear_on_submit=True, border=True):
    c1, c2 = st.columns([3, 1])
    new_name = c1.text_input("아이템", placeholder="예: 우유")
    new_qty = c2.number_input("수량", min_value=1, value=1, step=1)
    added = st.form_submit_button("＋ 추가", type="primary", use_container_width=True)
if added:
    if new_name.strip():
        add_item(new_name.strip(), int(new_qty))
        st.rerun()
    else:
        st.error("아이템 이름을 입력해 주세요.")

st.write("")

# 목록 영역 (F2 수정, F3 삭제, F4 체크, F5 진행 현황)
shopping_items = st.session_state.shopping_items

if not shopping_items:
    st.markdown(
        """
        <div class="empty-state">
            <div class="emoji">🧺</div>
            <div class="title">목록이 비어 있어요</div>
            <div>위에서 아이템을 추가해 보세요!</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    total = len(shopping_items)
    done = sum(1 for i in shopping_items if i["checked"])
    st.progress(done / total, text=f"**완료 {done} / 전체 {total}**  ({done * 100 // total}%)")

    for item in shopping_items:
        iid = item["id"]

        with st.container(border=True):
            if st.session_state.editing == iid:
                # 수정 모드
                with st.form(f"edit_form_{iid}", border=False):
                    e1, e2 = st.columns([3, 1])
                    edit_name = e1.text_input("이름", value=item["name"])
                    edit_qty = e2.number_input("수량", min_value=1, value=item["qty"], step=1)
                    b1, b2 = st.columns(2)
                    saved = b1.form_submit_button("저장", type="primary", use_container_width=True)
                    canceled = b2.form_submit_button("취소", use_container_width=True)
                if saved:
                    if edit_name.strip():
                        update_item(iid, edit_name.strip(), int(edit_qty))
                        st.session_state.editing = None
                        st.rerun()
                    else:
                        st.error("이름을 입력해 주세요.")
                elif canceled:
                    st.session_state.editing = None
                    st.rerun()
            else:
                # 일반 모드
                col_chk, col_edit, col_del = st.columns([6, 1, 1], vertical_alignment="center")
                label = f"{escape_md(item['name'])} ×{item['qty']}"
                if item["checked"]:
                    label = f":gray[~~{label}~~]"  # 흐린 색 + 취소선
                col_chk.checkbox(
                    label,
                    value=item["checked"],
                    key=f"chk_{iid}",
                    on_change=toggle_item,
                    args=(iid,),
                )
                if col_edit.button("✏️", key=f"edit_{iid}", help="수정", type="tertiary"):
                    st.session_state.editing = iid
                    st.rerun()
                if col_del.button("🗑️", key=f"del_{iid}", help="삭제", type="tertiary"):
                    delete_item(iid)
                    st.rerun()

    st.write("")
    # 하단 버튼 영역 (F6)
    has_checked = done > 0
    if st.button("완료 항목 삭제", disabled=not has_checked, use_container_width=True):
        clear_checked()
        st.rerun()
