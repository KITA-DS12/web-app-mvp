import { PostList } from './components/PostList';
import { usePosts } from './hooks/usePosts';

function App() {
  const { posts, loading, error, createPost, refetch } = usePosts();

  return (
    <div style={{ padding: '20px' }}>
      <h1>FastAPI + React Posts App</h1>
      <PostList 
        posts={posts}
        loading={loading}
        error={error}
        onCreatePost={createPost}
      />
    </div>
  );
}

export default App;