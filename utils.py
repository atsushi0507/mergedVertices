import ROOT as r

def trackCleaning(tree, idv):
    # Return tracks which pass the cleaning criteria
    # Input : TTree
    track = []
    m_pion = 139.57*0.001 # GeV
    for itrack in range(len(tree.dvtrack_ptWrtDV)):
        if ( (tree.DV_index[idv] != tree.dvtrack_DVIndex[itrack])):
            continue
        if (tree.dvtrack_failedExtrapolation[itrack] == 1):
            continue
        if (tree.dvtrack_isAssociated[itrack]):
            if (tree.dvtrack_ptWrtDV[itrack] < 2.):
                continue
            if ( (tree.DV_rxy[idv] > 85.5) and (tree.dvtrack_ptWrtDV[itrack] < 3.) ):
                continue
        # d0-significance
        d0sig = r.TMath.Abs(tree.dvtrack_d0[itrack]/tree.dvtrack_errd0[itrack])
        if ( (tree.DV_rxy[idv] < 23.5) and (d0sig < 15.)):
            continue
        if ( (tree.DV_rxy[idv] < 119.3) and (d0sig < 10.)):
            continue
        if ( (tree.DV_rxy[idv] > 119.3) and (d0sig < 10.) and tree.dvtrack_isAssociated[itrack] == 0):
            continue
        track.append([tree.dvtrack_ptWrtDV[itrack],
                      tree.dvtrack_etaWrtDV[itrack],
                      tree.dvtrack_phiWrtDV[itrack],
                      m_pion,
                      tree.dvtrack_isAssociated[itrack] ])
    return track

def getDVtracks(tracks):
    # Return TLorentzVector of the tracks of the DV
    dvtracks = r.TLorentzVector()
    nTracks = 0
    nTracksSel = 0
    for dvtrack in tracks:
        track = r.TLorentzVector()
        track.SetPtEtaPhiM(dvtrack[0],
                           dvtrack[1],
                           dvtrack[2],
                           dvtrack[3])
        dvtracks += track
        nTracks += 1
        if (dvtrack[4] == 0):
            nTracksSel += 1
    return dvtracks, nTracks, nTracksSel

def getEvents(tree, eventID, doUnblind):
    events = []
    for entry in range(tree.GetEntries()):
        ientry = tree.LoadTree(entry)
        if ientry < 0:
            break
        nb = tree.GetEntry(ientry)
        if nb <= 0:
            continue

        vertex = []
        covariance = []
        jets = []
        tracks = []
        for idv in range(tree.DV_n):
            if (not tree.DV_passFiducialCut[idv]):
                continue
            if (not tree.DV_passDistCut[idv]):
                continue
            if (not tree.DV_passChiSqCut[idv]):
                continue
            if (not tree.DV_passMaterialVeto[idv]):
                continue
            if (not tree.DV_passMaterialVeto_strict[idv]):
                continue
            if (tree.DV_m[idv] > 10. and tree.DV_nTracks[idv] >= 5):
                continue
            if (tree.DV_rxy[idv] < 22.):
                if (tree.DV_m[idv] > 10. and tree.DV_nTracksSel[idv] >= 5):
                    continue
            if (tree.DV_nTracks[idv] < 2 or tree.DV_nTracksSel[idv] < 2):
                continue
            vertex.append([tree.DV_x[idv], tree.DV_y[idv], tree.DV_z[idv], tree.DV_m[idv], tree.DV_rxy[idv], tree.DV_nTracks[idv], tree.DV_nTracksSel[idv]])
            eventID += 1
            track = trackCleaning(tree, idv)
            tracks.append(track)
        if (len(vertex) == 0):
            continue
        events.append([eventID, vertex, tracks])
    return events
