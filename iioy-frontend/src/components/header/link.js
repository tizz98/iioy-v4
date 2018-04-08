import { h, component } from 'fpreact';
import { Link } from 'preact-router/match';
import { NavItem } from 'mdbreact';

const initialModel = {
	active: false,
	href: null,
	children: null,
};
const Msg = {
	setHref: 0,
	setActive: 1,
	setChildren: 2,
};
const HeaderItemLink = component({
	props(props, dispatch) {
		dispatch(Msg.setHref)(props.href);
		dispatch(Msg.setActive)(props.active);
		dispatch(Msg.setChildren)(props.children);
	},

	update(model = initialModel, msg) {
		switch (msg.kind) {
			case Msg.setHref:
				return { ...model, href: msg.value };
			case Msg.setActive:
				return { ...model, active: msg.value };
			case Msg.setChildren:
				return { ...model, children: msg.value };
		}

		return model;
	},

	view(model, dispatch) {
		return (
			<NavItem active={ model.active }>
				<Link className="nav-link waves-effect waves-light" href={ model.href }>
					{ model.children }
				</Link>
			</NavItem>
		);
	},
});

export default HeaderItemLink;
