
inductive plane_tree
| node : list plane_tree → plane_tree

open plane_tree

def list_plane_tree_to_plane_tree : list plane_tree → plane_tree
| [] => node []
| tr :: trs => node (tr :: trs)

def plane_tree_to_list_plane_trees : plane_tree → list plane_tree
| node [] => []
| node (tr :: trs) => tr :: trs

def list_plane_tree_equiv_plane_tree : list plane tree ≃ plane_tree :=
{ to_fun := list_plane_tree_to_plane_tree,
  inv_fun := plane_tree_to_list_plane_trees,
  left_inv :=
    begin
      intro ls,
      cases ls with hd tl,
      { simp [list_plane_tree_to_plane_tree, plane_tree_to_list_plane_trees] },
      { simp [plane_tree_to_list_plane_trees, list_plane_tree_to_plane_tree] }
    end,
  right_inv :=
    begin
      intro T,
      cases T with ts,
      { induction ts with tr trs ih,
        { simp [plane_tree_to_list_plane_trees, list_plane_tree_to_plane_tree] },
        { simp [plane_tree_to_list_plane_trees, list_plane_tree_to_plane_tree] }
      }
    end }
