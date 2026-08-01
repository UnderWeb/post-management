// frontend/src/pages/PostsPage.tsx
/**
 * Main page component for managing and viewing posts.
 */
import { useEffect, useState } from 'react';
import { useAppDispatch, useAppSelector } from '../hooks';
import { fetchPosts } from '../features/posts/postsThunks';
import CreatePostForm from '../features/posts/components/CreatePostForm';
import PostList from '../features/posts/components/PostList';

function PostsPage() {
  const dispatch = useAppDispatch();
  const posts = useAppSelector((state) => state.posts.items);
  const loading = useAppSelector((state) => state.posts.loading);
  const error = useAppSelector((state) => state.posts.error);

  const [filter, setFilter] = useState('');

  // Requisito: Filtrar posts por nombre/título (búsqueda local)
  const filteredPosts = posts.filter((post) =>
    post.title.toLowerCase().includes(filter.toLowerCase())
  );

  useEffect(() => {
    dispatch(fetchPosts());
  }, [dispatch]);

  return (
    <main className="posts-page">
      <h1>Posts</h1>

      <section className="search-bar">
        <input
          className="form-input"
          placeholder="Filtrar por título..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        />
      </section>

      {loading && <p>Cargando posts...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {!loading && !error && filteredPosts.length === 0 && (
        <p>No existen posts.</p>
      )}

      {!loading && !error && filteredPosts.length > 0 && (
        <PostList posts={filteredPosts} />
      )}

      <CreatePostForm />
    </main>
  );
}

export default PostsPage;
