// src/components/ErrorMessage.tsx
interface Props {
  message: string;
}

function ErrorMessage({ message }: Props) {
  return <p role="alert">{message}</p>;
}

export default ErrorMessage;
