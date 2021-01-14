import ROOT as r
import numpy as np
from scipy.spatial import distance

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
        for ijet in range(len(tree.jet_pt)):
            jets.append([tree.jet_pt[ijet], tree.jet_eta[ijet], tree.jet_phi[ijet], tree.jet_m[ijet]*0.001])
            
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
            if (not doUnblind):
                if (tree.DV_m[idv] > 10. and tree.DV_nTracks[idv] >= 5):
                    continue
                if (tree.DV_m[idv] > 20. and tree.DV_nTracks[idv] == 4):
                    continue
                if (tree.DV_rxy[idv] < 22.):
                    if (tree.DV_m[idv] > 10. and tree.DV_nTracksSel[idv] >= 5):
                        continue
            if (tree.DV_nTracks[idv] < 2 or tree.DV_nTracksSel[idv] < 2):
                continue
            vertex.append([tree.DV_x[idv], tree.DV_y[idv], tree.DV_z[idv], tree.DV_m[idv], tree.DV_rxy[idv], tree.DV_nTracks[idv], tree.DV_nTracksSel[idv]])
            covariance.append([tree.cov0[idv], tree.cov1[idv], tree.cov2[idv], tree.cov3[idv], tree.cov4[idv], tree.cov5[idv]])
            eventID += 1
            track = trackCleaning(tree, idv)
            tracks.append(track)
        if (len(vertex) == 0):
            continue
        events.append([eventID, vertex, tracks, covariance, jets])
    return events

def getRegion(rxy):
    region = -1
    if (rxy < 25.):
        region = 0
    if (rxy >= 25. and rxy < 38.):
        region = 1
    if (rxy >= 38. and rxy < 145.):
        region = 2
    if (rxy >= 145. and rxy < 300.):
        region = 3
    return region

def getDVMatrix(dv):
    dvmatrix = np.matrix([dv[0], dv[1], dv[2]])
    return dvmatrix

def getCovarianceMatrix(cov):
    cov_matrix = np.matrix([[cov[0], cov[1], cov[3]],
                            [cov[1], cov[2], cov[4]],
                            [cov[3], cov[4], cov[5]]])
    return cov_matrix

def getDistance(dv1, dv2):
    distance = dv1 - dv2
    transpose = distance.T
    dist = r.TMath.Sqrt(distance*transpose)
    return dist

def getSignificance(dv1, dv2, cov1, cov2):
    sumCov = cov1 + cov2
    sig = distance.mahalanobis(dv1, dv2, sumCov.I)
    return sig

def getClosestJet(dv, jets):
    closeJet = r.TLorentzVector()
    min_dR = 1e10
    min_ijet = -1
    min_dEta = 1e10
    min_dPhi = 1e10

    dv_x, dv_y, dv_z = dv[0], dv[1], dv[2]
    dv_r = r.TMath.Sqrt(dv_x*dv_x + dv_y*dv_y + dv_z*dv_z)
    dv_phi = r.TMath.ATan2(dv_y, dv_x)
    dv_eta = r.TMath.ATanH(dv_z/dv_r)

    DV = r.TVector3()
    DV.SetXYZ(dv[0], dv[1], dv[2])
    nJets = len(jets)
    for ijet in range(nJets):
        dEta = (jets[ijet][1] - dv_eta)
        dPhi = (jets[ijet][2] - dv_phi)
        if (dPhi >= r.TMath.Pi()):
            dPhi -= 2*r.TMath.Pi()
        if (dPhi < -r.TMath.Pi()):
            dPhi += 2*r.TMath.Pi()
        dR = r.TMath.Sqrt(dEta*dEta + dPhi*dPhi)
        if (dR < min_dR):
            min_dR = dR
            min_ijet = ijet
            min_dEta = dEta
            min_dPhi = dPhi
    closeJet.SetPtEtaPhiM(jets[min_ijet][0], jets[min_ijet][1], jets[min_ijet][2], jets[min_ijet][3])
    return closeJet

def getDVTracks(dvtracks):
    DVtracks = r.TLorentzVector()
    nTracks, nTracksSel = 0, 0
    for itrack in dvtracks:
        track = r.TLorentzVector()
        track.SetPtEtaPhiM(itrack[0], itrack[1], itrack[2], itrack[3])
        DVtracks += track
        nTracks += 1
        if (itrack[4] == 0):
            nTracksSel += 1
    return DVtracks, nTracks, nTracksSel
