// src/features/posts/components/PostCard.tsx
import {
  useAppDispatch,
} from '../../../hooks';
import {
  removePost,
} from '../postsThunks';
import type {
  Post,
} from '../types';

interface PostCardProps {
  post: Post;
}

function PostCard(
  {
    post,
  }: PostCardProps,
) {
  const dispatch = useAppDispatch();

  function handleDelete() {
    dispatch(
      removePost(post.id),
    );
  }

  return (
    <article>
      <h2>
        {post.nombre}
      </h2>
      <p>
        {post.descripcion}
      </p>
      {
        post.resumen && (
          <pre>
            {JSON.stringify(
              post.resumen,
              null,
              2,
            )}
          </pre>
        )
      }
      <small>
        {
          new Date(
            post.fecha_creacion,
          ).toLocaleString()
        }
      </small>
      <button
        type='button'
        onClick={handleDelete}
      >
        Eliminar
      </button>
    </article>
  );
}

export default PostCard;
