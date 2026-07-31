// src/pages/PostsPage.tsx
import {
  useEffect,
} from 'react';
import {
  useAppDispatch,
  useAppSelector,
} from '../hooks';
import {
  fetchPosts,
} from '../features/posts/postsThunks';
import CreatePostForm from '../features/posts/components/CreatePostForm';
import PostList from '../features/posts/components/PostList';

function PostsPage() {
  const dispatch = useAppDispatch();

  const posts = useAppSelector(
    (state) => state.posts.items,
  );

  const loading = useAppSelector(
    (state) => state.posts.loading,
  );

  const error = useAppSelector(
    (state) => state.posts.error,
  );

  useEffect(
    () => {
      dispatch(
        fetchPosts(),
      );
    },
    [dispatch],
  );

  return (
    <main>
      <h1>
        Posts
      </h1>
      <CreatePostForm />
      {
        loading && (
          <p>
            Cargando posts...
          </p>
        )
      }
      {
        error && (
          <p>
            Error:
            {' '}
            {error}
          </p>
        )
      }
      {
        !loading &&
        !error &&
        posts.length === 0 && (
          <p>
            No existen posts.
          </p>
        )
      }
      {
        !loading &&
        !error &&
        posts.length > 0 && (
          <PostList
            posts={posts}
          />
        )
      }
    </main>
  );
}

export default PostsPage;
