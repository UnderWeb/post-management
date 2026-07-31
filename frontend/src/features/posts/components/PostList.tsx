// src/features/posts/components/PostList.tsx
import PostCard from './PostCard';

import type { Post } from '../../../types/post';

interface Props {
  posts: Post[];
}

function PostList({ posts }: Props) {
  return (
    <section>
      {posts.map((post) => (
        <PostCard
          key={post.id}
          post={post}
        />
      ))}
    </section>
  );
}

export default PostList;
