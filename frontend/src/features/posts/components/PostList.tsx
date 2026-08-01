// src/features/posts/components/PostList.tsx

import PostCard from './PostCard';
import type { Post } from '../../../types/post';


interface Props {
  posts: Post[];
}


function PostList({
  posts,
}: Props) {

  return (
    <table className="posts-table">

      <thead>
        <tr>
          <th>
            Nombre
          </th>

          <th>
            Descripción
          </th>

          <th>
            Acción
          </th>
        </tr>
      </thead>


      <tbody>

        {
          posts.map(
            (post) => (
              <PostCard
                key={post.id}
                post={post}
              />
            ),
          )
        }

      </tbody>

    </table>
  );
}


export default PostList;
