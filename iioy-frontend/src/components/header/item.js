import { h, component } from 'fpreact';
import { Match } from 'preact-router/match';
import ItemLink from './link';

const initialModel = {
	path: null,
	children: null,
};
const Msg = {
	setPath: 0,
	setChildren: 1,
};
const HeaderItem = component({
	props(props, dispatch) {
		dispatch(Msg.setChildren)(props.children);
		dispatch(Msg.setPath)(props.path);
	},

	update(model = initialModel, msg) {
		switch(msg.kind) {
			case Msg.setChildren:
				return { ...model, children: msg.value };
			case Msg.setPath:
				return { ...model, path: msg.value };
		}
		return model;
	},

	view(model, dispatch) {
		return (
			<Match path={ model.path }>
				{
					({ matches }) => (
						<ItemLink active={ matches } href={ model.path }>
							{ model.children }
						</ItemLink>
					)
				}
			</Match>
		);
	},
});

export default HeaderItem;
