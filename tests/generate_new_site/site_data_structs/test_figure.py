from unittest import mock
from unittest.mock import patch
from src.generate_new_site.site_data_structs import figure
from pathlib import Path


###################################
# Figure method integration tests #
###################################

def test_figures_register_and_gets():
    figures = figure.Figures(parent=mock.Mock())
    figs = {i: figure.Figure(
        figure_num=i,
        caption=None,
        img_orig_path=None,
        figure_path=Path("figpath{}".format(i)),
        path=None,
        parent=figures,
        orig_width=0,
        orig_height=0
    ) for i in range(4)}
    for fig in figs.values():
        figures.register(fig)

    for key, val in figs.items():
        assert figures.get_figure(key) == val
        assert figures.get_figure_num(Path("figpath{}".format(key))) == val.figure_num


######################
# Test update_href() #
######################

@patch('src.generate_new_site.utilities.path_ops.rel_path', return_value=Path("updated"))
def test_figure_update_href(mock_rel_path):
    # Mock parent
    figures = mock.Mock()
    figures.parent.pathtable.get_path = mock.Mock(return_value=Path("tablepath"))

    # Instantiate figure
    fig = figure.Figure(
        figure_num=1,
        caption=None,
        img_orig_path=Path("imgorig"),
        figure_path=Path("figpath"),
        path=Path("newfigpath"),
        parent=figures,
        orig_width=0,
        orig_height=0
    )
    clickable_areas = [
        figure.ClickableArea(
            x1=0,
            y1=0,
            x2=0,
            y2=0,
            orig_href=Path("orighref"),
            parent=fig
        ) for i in range(4)]
    fig.clickable_areas = clickable_areas

    # Test
    fig.update_href(Path("test"))

    assert fig.href == Path("updated").as_posix()
    assert fig.img_path == Path("updated").as_posix()
    for ce in clickable_areas:
        assert ce.href == Path("updated").as_posix()
