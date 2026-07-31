// src/pages/PostsPage.tsx
import { useEffect } from 'react';
import EmptyState from '../components/EmptyState';
import ErrorMessage from '../components/ErrorMessage';
import Loading from '../components/Loading';
import PostList from '../features/posts/components/PostList';
import { useAppDispatch, useAppSelector } from '../hooks';
import {
  selectPosts,
  selectPostsError,
  selectPostsLoading,
} from '../features/posts/postsSelectors';
import { fetchPosts } from '../features/posts/postsThunks';

function PostsPage() {
  const dispatch = useAppDispatch();

  const posts = useAppSelector(selectPosts);
  const loading = useAppSelector(selectPostsLoading);
  const error = useAppSelector(selectPostsError);


  useEffect(() => {
    dispatch(fetchPosts());
  }, [dispatch]);


  if (loading) {
    return <Loading />;
  }


  if (error) {
    return (
      <ErrorMessage message={error} />
    );
  }


  if (posts.length === 0) {
    return <EmptyState />;
  }


  return (
    <main>
      <h1>Posts</h1>

      <PostList posts={posts} />
    </main>
  );
}


export default PostsPage;
