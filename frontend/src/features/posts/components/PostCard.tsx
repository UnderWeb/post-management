// frontend/src/features/posts/components/PostCard.tsx
/**
 * Component to display a single post row in the table.
 */
import { useAppDispatch } from '../../../hooks';
import { removePost } from '../postsThunks';
import type { Post } from '../../../types/post';

interface Props {
  post: Post;
}

function PostCard({ post }: Props) {
  const dispatch = useAppDispatch();

  function handleDelete() {
    dispatch(removePost(post.id));
  }

  return (
    <tr>
      <td>{post.title}</td>
      <td>{post.description}</td>
      <td>
        {post.summary?.summary && (
          <small style={{ display: 'block', color: '#666', marginBottom: '4px' }}>
            Resumen: {post.summary.summary}
          </small>
        )}
        <button className="delete-button" onClick={handleDelete}>
          Eliminar
        </button>
      </td>
    </tr>
  );
}

export default PostCard;
