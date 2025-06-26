import { useState } from 'react';

export function PostList({ posts, loading, error, onCreatePost }) {
  const [text, setText] = useState('');
  const [creating, setCreating] = useState(false);
  const [createError, setCreateError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!text.trim()) {
      setCreateError('テキストを入力してください');
      return;
    }

    if (text.length > 255) {
      setCreateError('テキストは255文字以内で入力してください');
      return;
    }

    setCreating(true);
    setCreateError('');
    
    const result = await onCreatePost(text);
    
    if (result.success) {
      setText('');
    } else {
      setCreateError(result.error);
    }
    
    setCreating(false);
  };

  if (loading) return <div>読み込み中...</div>;
  if (error) return <div>エラー: {error}</div>;

  return (
    <div>
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <div>
          <input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="投稿内容を入力"
            style={{ 
              width: '300px', 
              padding: '8px',
              marginRight: '10px'
            }}
            disabled={creating}
          />
          <button type="submit" disabled={creating}>
            {creating ? '投稿中...' : '投稿'}
          </button>
        </div>
        {createError && (
          <div style={{ color: 'red', marginTop: '5px' }}>
            {createError}
          </div>
        )}
      </form>

      <div>
        <h2>投稿一覧</h2>
        {posts.length === 0 ? (
          <p>投稿がありません</p>
        ) : (
          <ul>
            {posts.map(post => (
              <li key={post.id}>
                {post.text} (ID: {post.id})
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}