"""KiCad10 native zone helpers; no implicit saves, no rule/exception changes.

Caller owns all authorization, matrix clipping and actual-board verification.
Coordinates mm. Holes are indexed per outline; do not discard them.
"""
import pcbnew as k

def poly_from_rings(outlines_mm, holes_by_outline_mm=None):
    holes_by_outline_mm=holes_by_outline_mm or [[] for _ in outlines_mm]
    assert len(outlines_mm)==len(holes_by_outline_mm)
    p=k.SHAPE_POLY_SET()
    for oi,vertices in enumerate(outlines_mm):
        assert len(vertices)>=3
        ix=p.NewOutline()
        for x,y in vertices:p.Append(k.FromMM(x),k.FromMM(y),ix,-1)
        for hole in holes_by_outline_mm[oi]:
            assert len(hole)>=3
            hi=p.NewHole(ix)
            for x,y in hole:p.Append(k.FromMM(x),k.FromMM(y),ix,hi)
    return p

def rings_from_poly(poly):
    def points(c):return [[k.ToMM(c.CPoint(i).x),k.ToMM(c.CPoint(i).y)] for i in range(c.PointCount())]
    return {
        'outlines_mm':[points(poly.COutline(i)) for i in range(poly.OutlineCount())],
        'holes_by_outline_mm':[[points(poly.CHole(i,h)) for h in range(poly.HoleCount(i))] for i in range(poly.OutlineCount())],
        'area_mm2':poly.Area()/1e12,
    }

def add_solid_zone(board, net, layer, poly, clearance_mm=.3, min_thickness_mm=.2, name=''):
    z=k.ZONE(board)
    z.SetLayer(layer)
    z.SetNetCode(net.GetNetCode())
    z.Outline().Append(poly)  # Copy into zone-owned polygon; SetOutline borrows SWIG lifetime.
    z.SetLocalClearance(k.FromMM(clearance_mm))
    z.SetMinThickness(k.FromMM(min_thickness_mm))
    z.SetPadConnection(k.ZONE_CONNECTION_FULL)
    # Native normal island-removal; synthetic fixture deliberately includes anchors.
    z.SetIslandRemovalMode(k.ISLAND_REMOVAL_MODE_ALWAYS)
    if name:z.SetZoneName(name)
    board.Add(z)
    return z

def refill_and_report(board):
    board.BuildConnectivity()
    ok=k.ZONE_FILLER(board).Fill(board.Zones())
    out=[]
    for z in board.Zones():
        layers={}
        for lay in [k.F_Cu,k.B_Cu]:
            if z.IsOnLayer(lay) and z.HasFilledPolysForLayer(lay):
                layers[board.GetLayerName(lay)]=rings_from_poly(z.GetFilledPolysList(lay))
        out.append({'uuid':z.m_Uuid.AsString(),'net':z.GetNetname(),'pad_connection':int(z.GetPadConnection()),'layers':layers})
    return {'fill_return':bool(ok),'zones':out}

def save_skipping_settings(path, board):
    # Explicit opt-in save; skip_settings=True prevents incidental project rewrites.
    return bool(k.SaveBoard(str(path),board,True))

