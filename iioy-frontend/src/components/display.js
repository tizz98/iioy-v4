import { h } from 'preact';

function isIterable(obj) {
    return typeof obj[Symbol.iterator] === 'function';
}

function Display(props) {
    const { children, when } = props;

    if (when) {
        let childComponent;
        if (children === null) {
            childComponent = null;
        } else if (typeof children === 'function') {
            childComponent = children();
        } else if (typeof children === 'string') {
            childComponent = <span>{ children }</span>;
        } else if (isIterable(children)) {
            childComponent = <span>{ children }</span>;
        } else {
            childComponent = children;
        }
        return childComponent;
    }

    return null;
}

export default Display;
