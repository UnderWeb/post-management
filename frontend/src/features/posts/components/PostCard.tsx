// src/features/posts/components/PostCard.tsx
import type { Post } from '../../../types/post';

interface Props {
  post: Post;
}

function PostCard({ post }: Props) {
  return (
    <article>
      <h2>{post.nombre}</h2>

      <p>
        {post.descripcion}
      </p>

      <small>
        {post.fecha_creacion}
      </small>
    </article>
  );
}

export default PostCard;
