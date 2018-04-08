import { h } from 'preact';
import Container, { COLORS } from './container';

export { COLORS };
export default ({ text, ...otherProps }) => (
    <Container { ...otherProps }>
        <h1 className="text-center align-self-center white-text">{ text }</h1>
    </Container>
);
