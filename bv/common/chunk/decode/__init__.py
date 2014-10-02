"""
    Chunk decoding
"""
import zlib

def decompress(decoder):
    """
    Decorator to factor out chunk
    decompression logic from decoder routines
    """
    def wrapper(self,blob,origin):
        return decoder(self,zlib.decompress(blob),origin)
    return wrapper

from panda3d.core import Geom,GeomVertexFormat
from panda3d.core import GeomTriangles,GeomNode

class Chunk2GeomDecoder:
    """
        Chunk decoder that decodes chunks to Panda3D Geoms/Nodes
    """
    def __init__(self):
        self.viewPoint=(0,0,0)
        self.cubeVerts=[
            # 14 vertices per cube mapped
            # so that UV coords utilize
            # the typical cube unwrap:
            #
            #   ####  <-- square texture
            #   ##U#
            #   BLFR
            #   ##D#    #=unused
            #
            # This form uses 14 vertices per cube since
            # the extra (worldspace overlapped) vertices
            # map different U,V coordinates at the same
            # worldspace coordinates, depending on face
            #   
            # x    y    z    u    v
            (1.00,1.00,1.00,0.00,0.50), # A
            (1.00,1.00,0.00,0.00,0.25), # B
            (0.00,1.00,1.00,0.25,0.50), # C
            (0.00,1.00,0.00,0.25,0.25), # D
            (0.00,0.00,1.00,0.50,0.50), # E
            (0.00,0.00,0.00,0.50,0.25), # F
            (1.00,0.00,1.00,0.75,0.50), # G
            (1.00,0.00,0.00,0.75,0.25), # H
            (1.00,1.00,1.00,1.00,0.50), # I
            (1.00,1.00,0.00,1.00,0.25), # J
            (0.00,1.00,1.00,0.50,0.75), # K
            (1.00,1.00,1.00,0.75,0.75), # L
            (0.00,1.00,0.00,0.50,0.00), # M
            (1.00,1.00,0.00,0.75,0.00)  # N
            #
            #  Faces (QUAD/TRIPAIR)
            #  using RHR vertex ordering for
            #  correct face surface normals
            #
            #    front: EFHG/EFH+HGE
            #     rear: CABD/CAB+BDC
            #     left: CDFE/CDF+FEC
            #    right: GHJI/GHJ+JIG
            #    upper: KEGL/KEG+GLK
            #    lower: FMNH/FMN+NHF
            #
        ]
        # Generate vertices for 1x1x256 'sliver'
        # starting at bottom (z=0), towards top (z=255)

    def setViewpoint(x,y,z):
        self.viewPoint=(x,y,z)

    @decompress
    def Chunk2Geom(self,chunk,origin):
        """
        Decodes chunk into Panda3D geometry format
        @param
            chunk: encoded chunk
            origin: chunk destination in world coordinates
            viewpoint: viewer reference point in world coordinates
                        (used for LOS culling of non-visible blocks
                        to reduce triangle load)
        @return
            A panda3D Node object translated appropriately to place
            the decoded chunk correctly within the world.
        """
        # determine where chunk should be placed in world space
        orgX=origin[0]
        orgY=origin[1]
        orgZ=origin[2]
        # determine chunk's coordinate
        chunkX=orgX/16
        chnukY=orgY/16
        # generate name tags for the various parts
        chunkId="%s_%s" % (chunkX,chunkY)
        vtxName="vtx_%s" % chunkId
        nodeName="node_%s" % chunkId
        # TODO: read chunk data and generate triangles

if __name__ == '__main__':
    pass
